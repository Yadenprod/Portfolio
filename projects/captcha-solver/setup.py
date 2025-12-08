from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="captcha-solver-pro",
    version="1.0.0",
    author="CapchaProd Team",
    author_email="team@captchaprod.com",
    description="Мощная система для распознавания капчи с использованием множественных подходов ИИ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/captchaprod/captcha-solver",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "gpu": [
            "tensorflow-gpu>=2.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "captcha-solver=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "captcha_solver": ["*.py"],
    },
) 