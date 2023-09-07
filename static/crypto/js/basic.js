const logout_user_user = window.location.origin + "/api/v1/logout/"

window.addEventListener('load', () => {
    const loader = document.querySelector('.loader');

    loader.classList.add('loader-hidden');

    loader.addEventListener('transitionend', () => {
        loader.remove()
    })
})

$(window).on('load', function (){
    toastr.options = {
      "closeButton": true,
      "debug": false,
      "newestOnTop": false,
      "progressBar": false,
      "positionClass": "toast-bottom-right",
      "preventDuplicates": false,
      "onclick": null,
      "showDuration": "300",
      "hideDuration": "1000",
      "timeOut": "5000",
      "extendedTimeOut": "1000",
      "showEasing": "swing",
      "hideEasing": "linear",
      "showMethod": "fadeIn",
      "hideMethod": "fadeOut"
    }})


function logout_user(){
    $.ajax({
        method: "POST",
        url: logout_user_user,
        success: function (){
            window.location.reload()
        }
    })
}