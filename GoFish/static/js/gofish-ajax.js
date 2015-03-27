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
            var atr = data.split(";");
            if (atr[0] == "true") {
                $('#creator').html(atr[1]);
            }
            else {
                $('#response').html(atr[1]);
            }
            $('#users').empty();
            $('#users').html(atr[2]);
        }
    });
    setTimeout("refresh()", 2500);
}
var re = true;
function refresh2() {
    $.ajax({
        type: "POST",
        url: "/ready2",
        data: {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                },
        success: function(data) {
            var atr = data.split(";");
            if (atr[0]=="True"){
                $('#play').show();
                if (re){
                    var users = $('#cards').empty();
                    $('#cards').html(atr[1]);
                    re = false;
                }
            }
            else{
                re = true;
                $('#play').hide();
                var users = $('#cards').empty();
                $('#cards').html(atr[1]);
            }
        }
    });
    setTimeout("refresh2()", 2500);
}



function create_post() {
    $.ajax({
        url : "/create_post/", // the endpoint
        type : "POST", // http method
        data : {
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            target : $('input[name=target]:checked', '#game').val(),
            wanted : $('input[name=wanted]:checked', '#game').val(),},

        // handle a successful response
        success : function(json) {
            $('#wanted').val(''); // remove the value from the input
            console.log(json)
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};