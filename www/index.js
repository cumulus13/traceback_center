function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
            // $("#table-responsive").load("index.html");
            $.ajax({
		      url : "/getall",
		      // dataType: "text",
		      // success : function (data) {
		      //    $(".text").html(data);
		      // }
		   });
		   // $("#table-responsive").load('App.js');
		   // console.log($("#traceback").html);
        }
    }, 1000);
}

window.onload = function () {
    var fiveMinutes = 10 * 1,
        display = document.querySelector('#time');
    startTimer(fiveMinutes, display);
};


let tabContainer = document.getElementById("tabs-466643");
let tabs = tabContainer = document.getElementsByClassName("nav-link");
let tabContent = document.getElementsByClassName("tab-content");

for (let i = 0; i < tabs.length; i++) {
	tabs[i].addEventListener("click", function() {
		let current = document.getElementsByClassName("active");
		current[0].className = current[0].className.replace(" active", "");
		tabContent[0].style.display = "none"
		
		this.className += " active";
		tabContent[i].style.display = "block"
	});
}

