

// var sup1 = new SuperGif({ gif: document.getElementById('example1') } );
// sup1.load();
// sup1.pause();
// sup1.play();
// sup1.move_to(0);
// sup1.move_relative(1)
// sup1.move_relative(-1)

  //test synth
var ready;
ready = function() {
    var sup1 = new SuperGif({ gif: document.getElementById('example1'), loop_mode: false } );
    sup1.load();

    var eventOutputContainer = document.getElementById("event");
    //var evtSrc = new EventSource("/subscribe");
    var evtSrc = new EventSource("http://127.0.0.1:5001/subscribe");

    evtSrc.onmessage = function(e) {
        console.log(e.data);
        eventOutputContainer.innerHTML = e.data;
        sup1.move_to(0);
        sup1.play();
    };


    }

document.addEventListener('DOMContentLoaded', ready);
