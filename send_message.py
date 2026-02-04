"""
Telegram Notification Service for IPO Data
Sends notifications for opening and closing IPOs to a Telegram channel
Uses MongoDB data stored by main.py
"""

import asyncio
import logging
import sys
from datetime import datetime
from typing import List, Dict, Any
import os

import telegram
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Configure logging
logging.basicConfig(
    level=getattr(logging, "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def validate_environment() -> None:
    """Validate required environment variables are set."""
    required_vars = [
        "MONGODB_URI",
        "DATABASE_NAME",
        "TELEGRAM_BOT_TOKEN",
        "CHANNEL_ID",
    ]
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
    Establish connection to MongoDB.

    Args:
        mongodb_uri: MongoDB connection string
        database_name: Name of the database to connect to

    Returns:
        AsyncIOMotorClient: Database connection object
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


def format_ipo_message(
    companyname: str,
    symbol: str,
    issuetype: str,
    issuefor: str,
    totalunit: str,
    issuemanager: str,
    openingdate: str,
    closingdate: str,
    perunitprice: str = "100",
    message_type: str = "opening",
) -> str:
    """
    Format IPO information into a readable Telegram message.

    Args:
        companyname: Name of the company
        symbol: Stock symbol
        issuetype: Type of issue (IPO/FPO/Debenture)
        issuefor: Target audience (General Public, etc.)
        totalunit: Total units available
        issuemanager: Name of issue manager
        openingdate: Opening date
        closingdate: Closing date
        perunitprice: Price per unit (optional)
        message_type: 'opening' or 'closing'

    Returns:
        Formatted message string
    """
    # Header based on message type
    if message_type == "opening":
        header = f"🔔 *NEW {issuetype.upper()} OPENING TODAY!*\n\n"
        intro = f"The {issuetype} of *{companyname}* ({symbol}) is opening today for {issuefor}. Don't miss this opportunity!\n"
    else:  # closing
        header = f"⏰ *LAST DAY TO APPLY!*\n\n"
        intro = f"Today is the final day to apply for the {issuetype} of *{companyname}* ({symbol}). Apply before it closes!\n"

    # Build details section
    details = f"\n📊 *{issuetype} Details:*\n"
    details += f"━━━━━━━━━━━━━━━━━━\n"
    details += f"🏢 *Company:* {companyname}\n"
    details += f"📈 *Symbol:* {symbol}\n"
    details += f"📋 *Issue Type:* {issuetype}\n"
    details += f"👥 *Issue For:* {issuefor}\n"

    # Format total units with commas if it's a number
    if totalunit and str(totalunit).replace(",", "").isdigit():
        formatted_units = f"{int(str(totalunit).replace(',', '')):,}"
        details += f"📦 *Total Units:* {formatted_units}\n"
    elif totalunit:
        details += f"📦 *Total Units:* {totalunit}\n"

    if perunitprice:
        details += f"💰 *Price/Unit:* Rs. {perunitprice}\n"

    details += f"🏦 *Issue Manager:* {issuemanager}\n"
    details += f"📅 *Opening Date:* {openingdate}\n"
    details += f"📅 *Closing Date:* {closingdate}\n"
    details += f"━━━━━━━━━━━━━━━━━━\n"

    # Footer
    if message_type == "opening":
        footer = "\n✅ Apply through your broker or online platform today!"
    else:
        footer = "\n⚠️ Don't miss out! Apply before the deadline!"

    return header + intro + details + footer


async def send_telegram_message(bot: telegram.Bot, message: str) -> bool:
    """
    Send message to Telegram channel.

    Args:
        bot: Telegram bot instance
        message: Message to send

    Returns:
        True if successful, False otherwise
    """
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
        logger.info("Message sent successfully to Telegram")
        return True
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False


async def process_ipo_notifications(
    records: List[Dict[str, Any]], message_type: str, bot: telegram.Bot
) -> int:
    """
    Process and send notifications for IPO records.

    Args:
        records: List of MongoDB documents
        message_type: 'opening' or 'closing'
        bot: Telegram bot instance

    Returns:
        Number of messages sent successfully
    """
    if not records:
        logger.info(f"No {message_type} IPOs found for today")
        return 0

    success_count = 0
    logger.info(f"Processing {len(records)} {message_type} IPO(s)")

    for record in records:
        try:
            # Extract fields from MongoDB document
            companyname = record.get("companyname", "Unknown")
            symbol = record.get("symbol", "N/A")
            issuetype = record.get("issuetype", "IPO")
            issuefor = record.get("issuefor", "General Public")
            totalunit = record.get("totalunit", "N/A")
            issuemanager = record.get("issuemanager", "N/A")
            openingdate = record.get("openingdate", "N/A")
            closingdate = record.get("closingdate", "N/A")
            perunitprice = record.get("perunitprice")

            # Format message
            message = format_ipo_message(
                companyname=companyname,
                symbol=symbol,
                issuetype=issuetype,
                issuefor=issuefor,
                totalunit=str(totalunit) if totalunit else "N/A",
                issuemanager=issuemanager,
                openingdate=str(openingdate),
                closingdate=str(closingdate),
                perunitprice=str(perunitprice) if perunitprice else None,
                message_type=message_type,
            )

            # Send message
            if await send_telegram_message(bot, message):
                success_count += 1
                logger.info(
                    f"Sent {message_type} notification for {companyname} ({symbol})"
                )

            # Small delay to avoid rate limiting
            await asyncio.sleep(1)

        except Exception as e:
            logger.error(
                f"Error processing record {record.get('symbol', 'Unknown')}: {e}"
            )
            continue

    logger.info(
        f"Successfully sent {success_count}/{len(records)} {message_type} notifications"
    )
    return success_count


async def main() -> None:
    """Main execution function."""
    try:
        logger.info("Starting IPO Telegram Notification Service")

        # Validate environment
        validate_environment()

        # Get current date
        today = datetime.now().date()
        day_name = today.strftime("%A")
        today_str = today.strftime("%Y-%m-%d")

        # Skip on Saturday
        if day_name == "Saturday":
            logger.info("Today is Saturday - skipping notifications")
            return

        logger.info(f"Processing notifications for {today_str} ({day_name})")

        # Initialize Telegram bot
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        logger.info("Telegram bot initialized")

        # Connect to MongoDB (same as main.py)
        assert MONGODB_URI is not None, "MONGODB_URI must be set"
        assert DATABASE_NAME is not None, "DATABASE_NAME must be set"
        db = await get_mongodb_connection(MONGODB_URI, DATABASE_NAME)

        collection = db["upcoming_ipodetails"]

        # Query for opening IPOs (openingdate matches today)
        opening_records = await collection.find({"openingdate": today_str}).to_list(
            length=None
        )

        # Query for closing IPOs (closingdate matches today)
        closing_records = await collection.find({"closingdate": today_str}).to_list(
            length=None
        )

        logger.info(
            f"Found {len(opening_records)} opening and {len(closing_records)} closing IPOs"
        )

        # Process notifications
        opening_sent = await process_ipo_notifications(opening_records, "opening", bot)
        closing_sent = await process_ipo_notifications(closing_records, "closing", bot)

        # Summary
        total_sent = opening_sent + closing_sent
        logger.info(
            f"Notification service completed: {total_sent} total messages sent "
            f"({opening_sent} opening, {closing_sent} closing)"
        )

    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
