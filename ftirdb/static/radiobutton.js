function changeSrc() {
    if (document.getElementById("onegraph").checked) {
    document.getElementById("picture").src = "http://localhost:6543/static/fig.png";
    } else if (document.getElementById("threegraphs").checked) {
    document.getElementById("picture").src = "http://localhost:6543/static/fig2.png"
    } else if (document.getElementById("twographs").checked) { 
    document.getElementById("picture").src = "http://localhost:6543/static/fig3.png";
    } else if (document.getElementById("fourgraphs").checked) { 
    document.getElementById("picture").src = "http://localhost:6543/static/fig4.png";
    }
}

function showMenu() {
     document.getElementsByClassName("menu")[0].style.display = "block";
}

