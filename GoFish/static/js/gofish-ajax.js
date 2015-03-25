
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
                //csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                //csrfmiddlewaretoken:'{{csrf_token}}',
                },
        success: function(data) {
            $('#response').html(data);
        }
    });
    setTimeout("refresh()", 3000);
}
