from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.routes import router

app = FastAPI()

app.include_router(router)


@app.get("/", response_class=HTMLResponse)
async def home():

    return """
<!DOCTYPE html>
<html>

<head>
<meta charset="utf-8">
<title>NNgo AI</title>

<style>

body{
    margin:0;
    font-family:Arial;
    background:#071226;
    color:white;
}

.container{
    padding:80px;
}

h1{
    font-size:70px;
    margin-bottom:40px;
}

input{
    width:500px;
    padding:20px;
    font-size:24px;
    border:none;
    border-radius:15px;
}

button{
    padding:20px 35px;
    font-size:24px;
    border:none;
    border-radius:15px;
    background:#2563eb;
    color:white;
    cursor:pointer;
    margin-left:10px;
}

button:hover{
    background:#1d4ed8;
}

</style>
</head>

<body>

<div class="container">

<h1>NNgo AI Route</h1>

<input
    id="prompt"
    placeholder="Куда хотите пойти?"
>

<button onclick="goRoute()">
    Найти маршрут
</button>

</div>

<script>

function goRoute(){

    const text =
        document.getElementById("prompt").value;

    window.location.href =
        "/routes/request?text="
        + encodeURIComponent(text);
}

</script>

</body>
</html>
"""