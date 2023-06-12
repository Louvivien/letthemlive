# Let Them Live - Social Media Automation

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<p align="center">
  <h3 align="center">Let Them Live</h3>

  <p align="center">
    By harnessing the power of AutoGPT and LangChain, we have created a platform that allows social media profiles to operate autonomously, creating a new breed of influencers - Auto-GPT Virtual Influencers.
    <br />
    <a href="https://github.com/Louvivien/letthemlive"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://lablab.ai/event/ai-agents-hackathon/let-them-live">View Project</a>
    ·
    <a href="https://github.com/Louvivien/letthemlive/issues">Report Bug</a>
    ·
    <a href="https://github.com/Louvivien/letthemlive/issues">Request Feature</a>
  </p>
</p>

![Python Version][python-image]
![License][license-image]

## Setup

1. Install Python 3.6 or later.

2. Install the required Python packages:

    ```bash
    pip install instagrapi python-dotenv
    ```

3. Clone this repository:

    ```bash
    git clone https://github.com/Louvivien/letthemlive.git
    cd letthemlive
    ```

4. Create a `.env` file in the root directory and add your Instagram username and password:

    ```bash
    INSTA_USERNAME=your_username
    INSTA_PASSWORD=your_password
    ```

5. Run the script:

    ```bash
    python main.py
    ```

## Usage

This script logs into Instagram using the provided username and password, finds a user by their username, and sends them a direct message. It uses AutoGPT and LangChain to automate the conversation with the user.

## Troubleshooting

If the script is not working as expected, check the following:

- Make sure your Instagram username and password are correct and the account is not locked or restricted.
- Check the console for any error messages.

## Ongoing work

The integration of AutoGPT, LangChain, and Instagram is complete. It can engage in a conversation, follow user based on a topic. 
We will add some other methods in instagram and add other social media. 

Currently adding method to generate images with DeamBooth model and Replicate. 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Distributed under the MIT License. See `LICENSE` for more information.

[python-image]: https://img.shields.io/badge/python-v3.6+-blue.svg
[license-image]: https://img.shields.io/badge/license-MIT-blue.svg

[contributors-shield]: https://img.shields.io/github/contributors/Louvivien/letthemlive.svg?style=for-the-badge
[contributors-url]: https://github.com/Louvivien/letthemlive/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Louvivien/letthemlive.svg?style=for-the-badge
[forks-url]: https://github.com/Louvivien/letthemlive/network/members
[stars-shield]: https://img.shields.io/github/stars/Louvivien/letthemlive.svg?style=for-the-badge
[stars-url]: https://github.com/Louvivien/letthemlive/stargazers
[issues-shield]: https://img.shields.io/github/issues/Louvivien/letthemlive.svg?style=for-the-badge
[issues-url]: https://github.com/Louvivien/letthemlive/issues
[license-shield]: https://img.shields.io/github/license/Louvivien/letthemlive.svg?style=for-the-badge
[license-url]: https://github.com/Louvivien/letthemlive/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
