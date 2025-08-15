from setuptools import setup, find_packages

setup(
    name="chat-to-excel",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Chat with Excel files using LLM technology",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "plotly>=5.17.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "groq>=0.4.0",
        "python-dotenv>=1.0.0",
        "xlrd>=2.0.0",
        "numpy>=1.24.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "chat-to-excel=app:main",
        ],
    },
) 