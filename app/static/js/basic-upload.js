$(function () {

    $(".js-upload-photos").click(function () {
        $("#fileupload").click();
    });

    $("#fileupload").fileupload({
        dataType: 'json',
        sequentialUploads: true,  /* 1. SEND THE FILES ONE BY ONE */
        start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
            $("#modal-progress").modal("show");
            // $('#gallery').removeClass('d-none')
        },
        stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
            console.log($("#modal-progress").find('.modal-title'))
            $("#modal-progress").find('.modal-title').text('Done!')
        },
        progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
            var progress = parseInt(data.loaded / data.total * 100, 10);
            var strProgress = progress + "%";
            $(".progress-bar").css({ "width": strProgress });
            $(".progress-bar").text(strProgress);
        },
        done: function (e, data) {
            if (data.result.is_valid) {
                const name = data.result.name
                const url = data.result.url
                const id = data.result.pet_id
                $("#gallery").prepend(`
                <div class="col-lg-3 col-md-4 col-xs-6">
                  <img class="img-fluid img-thumbnail" src="${url}" alt="${name.split('/').slice(-1)[0]}">
                </div>`)
            }
        }

    });

                //   <button class="delete-photo btn btn-link" data-photoname="${name}" data-petid="${id}">
                //     <span class="float-right">&times;</span>
                //   </button>

    $('.delete-photo').click(function(event) {
        event.preventDefault()
        const id = $(this).attr('data-petid')
        const photoname = $(this).attr('data-photoname')
        const url = '/pet/' + id + '/delete_photo/'
        $.post(url, { name: photoname }).done((response) => {
            $(this).parent().remove()
        })
    })

});