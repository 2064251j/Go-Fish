function refresh(gameID) {
    $.ajax({
        type: "POST",
        url: "{% url 'lobby' gameID%}",
        success: function(data) {
            $('#response').html(data);
        }
    });
    setInterval("refresh(gameID)", 1000);
}

$(function(gameID){
    refresh(gameID);
});