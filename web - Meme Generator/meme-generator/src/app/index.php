<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FCSC 2025 Meme Generator</title>
    <link rel="icon" type="image/x-icon" href="img/favicon.ico">
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .navbar { background-color: #007bff; color: white; padding: 10px; text-align: center; font-size: 1.5rem; font-weight: bold; }
        .main-container { display: flex; height: 90vh; padding: 20px; }
        .sidebar { width: 30%; overflow-y: auto; padding-right: 20px; }
        .content { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; }
        .meme-container { position: relative; text-align: center; margin-top: 20px; }
        .meme-text {
            position: absolute;
            width: 90%;
            top: 85%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 50px;
            font-weight: bold;
            color: white;
            text-transform: uppercase;
            text-shadow: -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000, 3px 3px 0 #000;
        }
        .meme-preview {
            width: 100px; /* Smaller images */
            height: auto;
            cursor: pointer;
            border: 3px solid transparent;
            transition: 0.3s;
            margin: 5px;
        }
        .meme-preview:hover, .selected { border-color: #007bff; }
        #selected-file { font-weight: bold; color: #007bff; text-align: center; }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            justify-items: center;
        }
    </style>
</head>
<body>

    <div class="navbar">FCSC 2025 Meme Generator</div>

    <div class="main-container">
        <div class="sidebar">
            <h5 class="text-center">Choose a meme</h5>
            <div class="grid-container">
                <?php
                $files = glob("img/*.{jpg,jpeg,png,gif}", GLOB_BRACE);
                foreach ($files as $file) {
                    $filename = basename($file);
                    echo "<label class='image-label'>
                    <input type='radio' name='image' value='$filename' hidden>
                    <img src='img/$filename' class='meme-preview'>
                    </label>";
                }
                ?>
            </div>
        </div>
        <div class="content">
            <p id="selected-file" class="mb-3"></p>
            <form action="" method="GET" style="width: 100%; max-width: 500px;">
                <input type="hidden" id="selected-image" name="image">
                <input type="text" id="text-input" name="text" class="form-control mb-3" placeholder="Enter meme text" required disabled>
                <button type="submit" id="generate-btn" class="btn btn-primary w-100" disabled>Generate Meme</button>
            </form>

            <?php if (isset($_GET['image']) && isset($_GET['text'])): ?>
            <div class="meme-container">
                <img src="img/<?php echo $_GET['image']; ?>" class="img-fluid">
                <div class="meme-text"><?php echo strtoupper($_GET['text']); ?></div>
            </div>
        <?php endif; ?>
    </div>
</div>
<script>
    document.querySelectorAll(".meme-preview").forEach(img => {
        img.addEventListener("click", function() {
            document.querySelectorAll(".meme-preview").forEach(i => i.classList.remove("selected"));
            this.classList.add("selected");
            let fileName = this.previousElementSibling.value;
            document.getElementById("selected-file").textContent = "Selected: " + fileName;
            document.getElementById("selected-image").value = fileName;
            document.getElementById("text-input").disabled = false;
            document.getElementById("generate-btn").disabled = false;
        });
    });
</script>
</body>
</html>
