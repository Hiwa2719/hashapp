
$(document).ready(function () {

    let hashForm = $('.hashForm form')

    //generate button
    let genButton = $('.generate')
    genButton.click(function(){

        $.ajax({
            url: '/hash-gen/',
            method: 'POST',
            data: form.serialize(),
            success: function (data){
                console.log('success')
            },
            error: function (errorData){
                console.log(errorData)
            }
        })
    })

    //Clear button
    let clearButton = $('.clear')
    clearButton.click(function (){
        hashForm[0].reset()
    })

    //save button
    let saveButton = $('.save')
    saveButton.click(function () {

        $.ajax({
            url: '/save-hash/',
            method: 'POST',
            data: hashForm.serialize(),
            success: function(data){
                console.log('succes')
            },
            error: function(errorData){
                console.log('Error')
            }
        })
    })

    // register/login button
    let authButton = $('.authentication .register, .login')
    authButton.click(function (event){
        event.preventDefault()
        let buttonText = $(this).text()
        $('.modal-body h5').text(buttonText)

        $.ajax({
            url: '/get-auth-form/',
            method: 'GET',
            data: {'button': buttonText},
            success: function (data){
                console.log('success')
                $('.modal-body').append(data.form)
                $('.modal-btn').click()
            },
            error: function (errorData){
                console.log('error')
                console.log(errorData)
            }
        })
    })

    // logout button
    let logoutButton = $('.authentication .logout')
    logoutButton.click(function(){
        $.ajax({
            url: '/logout/',
            method: 'GET',
            success: function (data){
                console.log('success logout')
                $('.modal-body .close').click()
                logoutButton.addClass('d-none')
                authButton.removeClass('d-none')
            },
            error: function (errorData){
                console.log('error')
            }
        })
    })
})
