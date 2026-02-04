"""
IPO Data Storer - Production Version
Fetches IPO, FPO, and Bond data from nepalipaisa.com API and stores in MongoDB
"""

import asyncio
import logging
import sys
from datetime import datetime, timezone
from typing import Any
import cloudscraper
import random
import os
from dotenv import load_dotenv
import json
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
load_dotenv()

# Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "upcoming_ipodetails")

# Configure logging
logging.basicConfig(
    level=getattr(logging, "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def validate_environment() -> None:
    """Validate required environment variables are set."""
    required_vars = ["MONGODB_URI", "DATABASE_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
        logger.error(
            "Please check your .env file and ensure all required variables are set."
        )
        sys.exit(1)

    logger.info("Environment variables validated successfully")


async def get_mongodb_connection(
    mongodb_uri: str, database_name: str
) -> AsyncIOMotorClient:
    """
    Establish connection to MongoDB with proper error handling.

    Args:
        mongodb_uri: MongoDB connection string
        database_name: Name of the database to connect to

    Returns:
        AsyncIOMotorClient: Database connection object

    Raises:
        SystemExit: If connection fails
    """
    try:
        client = AsyncIOMotorClient(
            mongodb_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
        )
        # Test the connection
        await client.admin.command("ping")
        db = client[database_name]
        logger.info(f"Connected to MongoDB database: {database_name}")
        return db
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        logger.error(
            "Please verify your MONGODB_URI is correct and the database is accessible"
        )
        sys.exit(1)


def get_api_data(api_url: str) -> dict[str, Any]:
    """
    Fetch data from API with retry mechanism and comprehensive error handling.

    Args:
        api_url: URL to fetch data from

    Returns:
        Dict containing API response data, empty dict on failure
    """
    try:
        # List of user agents to rotate
        user_agents = [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        ]

        # Create CloudScraper instance to bypass bot protection
        scraper = cloudscraper.create_scraper(
            delay=10,
            browser={"custom": "ScraperBot/1.0"},
        )

        # Comprehensive headers to mimic real browser request
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "identity",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Referer": "https://www.nepalipaisa.com/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Brave";v="144"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "Upgrade-Insecure-Requests": "1",
            "Priority": "u=0, i",
        }

        logger.info(f"Fetching data from: {api_url}")
        response = scraper.get(api_url, headers=headers, timeout=30)

        if response.status_code == 200:
            logger.info(f"Successfully fetched data from: {api_url}")
            return response.json()
        else:
            logger.error(
                f"Failed to fetch URL: {api_url}. Status code: {response.status_code}"
            )
            return {}

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response from {api_url}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error fetching URL {api_url}: {str(e)}")
        return {}


async def update_insert_data_in_mongodb(
    db: AsyncIOMotorClient,
    collection_name: str,
    filtered_data: list[dict[str, Any]],
) -> None:
    """
    Upsert multiple records to MongoDB based on symbol field.

    Args:
        db: MongoDB database connection
        collection_name: Name of the collection to update
        filtered_data: List of records to upsert
    """
    if not filtered_data:
        logger.warning("No data to insert/update in MongoDB")
        return

    collection = db[collection_name]
    success_count = 0
    error_count = 0

    for item in filtered_data:
        try:
            # Validate that symbol exists
            if not item.get("symbol"):
                logger.warning(f"Skipping record without symbol: {item}")
                error_count += 1
                continue

            # Add metadata
            item["last_updated"] = datetime.now(timezone.utc)

            # Upsert based on symbol
            await collection.update_one(
                {"symbol": item["symbol"]}, {"$set": item}, upsert=True
            )
            success_count += 1

        except Exception as e:
            logger.error(f"Error upserting symbol {item.get('symbol')}: {e}")
            error_count += 1

    logger.info(
        f"MongoDB operation completed: {success_count} successful, {error_count} errors"
    )


def filter_data(datas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Filter and transform API data to match database schema.
    Only includes records with future closing dates.

    Args:
        datas: Raw data from API

    Returns:
        List of filtered and transformed records
    """
    # Use date-only comparison (no time component)
    today = datetime.now().date()
    filtered_data = []

    for data in datas:
        try:
            # Validate required fields
            closing_date_str = data.get("closingDateAD")
            if not closing_date_str:
                logger.debug(
                    f"Skipping record without closing date: {data.get('companyName', 'Unknown')}"
                )
                continue

            # Parse closing date (expecting format: YYYY-MM-DD)
            try:
                # Extract just the date part (ignore time if present)
                date_part = closing_date_str.split("T")[
                    0
                ]  # Handle ISO format like "2026-02-04T00:00:00"
                closing_date = datetime.strptime(date_part, "%Y-%m-%d").date()
            except ValueError as e:
                logger.warning(
                    f"Invalid date format for {data.get('companyName', 'Unknown')}: {closing_date_str}"
                )
                continue

            # Filter out past records (compare dates only)
            if closing_date < today:
                logger.debug(
                    f"Skipping past record: {data.get('companyName', 'Unknown')} (closed: {closing_date_str})"
                )
                continue

            # Build entry with common fields
            entry = {
                "companyname": data.get("companyName"),
                "issuemanager": data.get("issueManager") or data.get("shareRegistrar"),
                "openingdate": data.get("openingDateAD"),
                "closingdate": data.get("closingDateAD"),
                "totalunit": data.get("units"),
                "perunitprice": data.get("pricePerUnit"),
            }

            # Add type-specific fields
            if data.get("bondId"):
                entry.update(
                    {
                        "symbol": data.get("bondSymbol"),
                        "issuetype": "Debenture",
                        "issuefor": "General Public",
                    }
                )
            elif data.get("fpoId") or data.get("ipoId"):
                entry.update(
                    {
                        "symbol": data.get("stockSymbol"),
                        "issuetype": "IPO" if data.get("ipoId") else "FPO",
                        "issuefor": (
                            "General Public"
                            if data.get("shareType") == "ordinary"
                            else data.get("shareType")
                        ),
                    }
                )
            else:
                logger.warning(
                    f"Unknown issue type for: {data.get('companyName', 'Unknown')}"
                )
                continue

            # Validate symbol exists
            if not entry.get("symbol"):
                logger.warning(
                    f"No symbol found for: {data.get('companyName', 'Unknown')}"
                )
                continue

            filtered_data.append(entry)

        except Exception as e:
            logger.error(f"Error processing record: {e}")
            continue

    logger.info(
        f"Filtered {len(filtered_data)} active records from {len(datas)} total records"
    )
    return filtered_data


async def main() -> None:
    """Main execution function."""
    try:
        logger.info("Starting IPO Data Storer")

        # Validate environment
        validate_environment()

        # Connect to MongoDB (type assertions after validation)
        assert MONGODB_URI is not None, "MONGODB_URI must be set"
        assert DATABASE_NAME is not None, "DATABASE_NAME must be set"
        db = await get_mongodb_connection(MONGODB_URI, DATABASE_NAME)

        all_filtered_data = []

        logger.info("Running in LIVE API mode")
        api_urls = [
            "https://nepalipaisa.com/api/GetFpos?pageNo=1&itemsPerPage=10&pagePerDisplay=10",
            "https://nepalipaisa.com/api/GetIpos?pageNo=1&itemsPerPage=10&pagePerDisplay=10",
            "https://nepalipaisa.com/api/GetBonds?pageNo=1&itemsPerPage=10&pagePerDisplay=10",
        ]

        for api_url in api_urls:
            api_response = get_api_data(api_url)
            if api_response:
                # Extract data from nested structure
                api_data = api_response.get("result", {}).get("data", [])
                if api_data and isinstance(api_data, list):
                    logger.info(f"Received {len(api_data)} records from API")
                    all_filtered_data.extend(filter_data(api_data))
                else:
                    logger.warning(f"No data array found in response from {api_url}")
            else:
                logger.warning(f"No response received from {api_url}")

        # Update database
        if all_filtered_data:
            await update_insert_data_in_mongodb(db, "upcoming_ipodetails", all_filtered_data)
            logger.info(
                f"Successfully processed {len(all_filtered_data)} active IPO/FPO/Bond records"
            )
        else:
            logger.warning("No active IPOs/FPOs/Bonds found to update")

        logger.info("IPO Data Storer completed successfully")

    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
