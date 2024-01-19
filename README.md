# AI Captcha Generator

## what is this?
CaptchaV1 is a project that is supposed to make captchas easier to integrate, making it easier to make your apps bot-resistant.
It is specifically aimed on faucets and games that use the Banano crypto.
## what is the plan for the future?
The plan in the integrate it with a Banano distribution game, where it would protect the game against botters.

## instructions

### without stable diffusion (not recommended)
1. make a folder called "generated_images" in the main directory.
2. add images, titled "<name>-<randomstring>.png". there should be 2-8 unique names, 6 is recommended. it doesn't matter what you put as the random string, as long as there is a "-" separating is from the name. the more files you put in the folder, the more random the captchas will be
3. run server.py
4. go to 127.0.0.1:8000/docs for the different api endpoints. example file is in web/html/index.html

### stable diffusion (recommended)
1. download and install stable diffusion web. this can be done here: https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. run it with the --api argument
3. verify it's running on 127.0.0.1:7860
4. make a directory called "generated_images" in the root
5. configure the wordlist in config.py. the wordlist you want to change is called `wordlistv2`. it is a dictionary in the format `{"prompt": "alias"}`. the prompt part will be inserted into stable diffusion, the alias part will be displayed in the captcha instructions.
6. run `python3 image_service.py`. this should start generating images.
7. once you have at least 9 images, you can run server.py
8. an example implementation can be found in web/html/index.html
