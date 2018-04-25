function del(url) {
    $.ajax({
        url: url, 
        type: 'DELETE',
        success: function (response) {
            location.replace(response)
        },
        error: function (err) {
            console.log(err)
        }
    })
}