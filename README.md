# IPO Data Storer

A production-ready Python application that fetches IPO, FPO, and Bond data from the Nepali Paisa API and stores it in MongoDB. The application automatically filters out expired offerings and maintains an up-to-date database of active investment opportunities.

## Features

- **Automated Data Collection**: Fetches data from Nepali Paisa API
- **Smart Filtering**: Automatically removes expired IPOs/FPOs/Bonds
- **MongoDB Integration**: Efficient upsert operations based on stock symbols
- **Retry Mechanism**: Automatic retry with exponential backoff for failed API calls
- **Comprehensive Logging**: Structured logging for monitoring and debugging
- **Environment-based Configuration**: Flexible configuration via environment variables
- **GitHub Actions Support**: Automated daily updates
- **Production-Ready**: Proper error handling, validation, and type hints

## Prerequisites

- Python 3.9 or higher
- MongoDB database (local or cloud-based like MongoDB Atlas)
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/santoshvandari/IPODataStorer.git
   cd IPODataStorer
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your MongoDB credentials:
   ```env
   MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/"
   DATABASE_NAME="ipo_database"
   ```

## Usage

### Running Locally

**Production Mode (Live API):**
```bash
python main.py
```

**Development Mode (Local JSON files):**
```bash
USE_LOCAL_FILES=true python main.py
```

### Running with GitHub Actions

The application includes a GitHub Actions workflow that runs automatically every day at midnight UTC.

**Setup GitHub Secrets:**

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `MONGODB_URI`: Your MongoDB connection string
   - `DATABASE_NAME`: Your database name

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

**Santosh Bhandari**
- GitHub: [@santoshvandari](https://github.com/santoshvandari)

## Acknowledgments

- Data provided by [Nepali Paisa](https://www.nepalipaisa.com/)
- Built with Python, MongoDB, and CloudScraper

---

**Note**: This application is for educational and informational purposes only. Always verify investment information from official sources before making financial decisions.
