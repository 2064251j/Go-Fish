var t = '';
var w = '';

function refresh() {
    var gId = $('#response').attr('game-id');
    var link = $('#response').attr('url');
    var players = $('#response').attr('users').split(',');
    $.ajax({
        type: "POST",
        url: link,
        data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                id: gId,
                users : players,
                },
        success: function(data) {
            $('#response').html(data);
        }
    });
    setTimeout("refresh()", 3000);
}

function play() {
    var gId = $('#response').attr('game-id');
    var link = $('#response').attr('url');
    $.ajax({
        type: "POST",
        url: link,
        data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                id: gId,
                target : t,
                wanted : w,
                },
        success: function(data) {
            $('#response').html(data);
        }
    });
    t = "";
    w = "";
}

function target() {
    t = event.target.id;
    alert(t);
    if (w != ""){
        play();
        alert("what");
    }
}
function wanted() {
    w = event.target.id;
    alert(w);
    if (t != ""){
        play();
        alert("what");
    }
}