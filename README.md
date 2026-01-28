# 🧴 SkinTelligent - AI-Powered Skincare Advisor

An intelligent skincare routine generator that provides personalized recommendations based on skin type, concerns, budget, and location. Features specialized support for Nigerian skincare needs.

## Features

- 🌍 **Global Skincare Routine Generator** - Personalized routines for any location
- 🧪 **Ingredient Checker** - Analyze product ingredients for comedogenic and fragrance allergens
- 🇳🇬 **Nigerian-Centered Skincare** - Specialized recommendations for Nigerian climate and products
- 🛍️ **Store Directory** - Curated list of skincare stores in Nigeria

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd skintelligent
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_actual_api_key_here
```

### 5. Run the Application

```bash
streamlit run app.py
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Yes |
| `OPENROUTER_BASE_URL` | API endpoint (default provided) | No |
| `DEFAULT_MODEL` | Default LLM model (default: claude-3-haiku) | No |
| `INGREDIENT_EXPLAINER_MODEL` | Model for ingredient analysis | No |

## Project Structure

```
skintelligent/
├── app.py                  # Main Streamlit application
├── utils.py                # Utility functions and data
├── prompt_utils.py         # Prompt generation functions
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not tracked)
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Security Notes

⚠️ **IMPORTANT**: Never commit the following files:
- `.env` - Contains your API keys
- `config.py` - If you create one with hardcoded secrets
- Any file with API keys or credentials

These files are already in `.gitignore` to prevent accidental commits.

## API Key Security

This project uses OpenRouter API. To get your API key:

1. Visit [OpenRouter](https://openrouter.ai/)
2. Create an account
3. Generate an API key
4. Add it to your `.env` file

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure no sensitive data is committed
5. Submit a pull request

## Features Roadmap

- [ ] User authentication
- [ ] Save routine history
- [ ] Product tracking
- [ ] Routine reminders
- [ ] Skin progress photos
- [ ] Community reviews

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or feedback, please open an issue on GitHub.

## Acknowledgments

- Built with Streamlit
- Powered by OpenRouter AI
- Designed for diverse skin tones and types
