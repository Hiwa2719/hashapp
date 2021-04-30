
$(document).ready(function () {

    let hashForm = $('.hashForm form')

    //generate button
    let genButton = $('.generate')
    genButton.click(function(){

        $.ajax({
            url: '/hash-gen/',
            method: 'POST',
            data: hashForm.serialize(),
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

    function registerLogin(event, thisObj, url){
        event.preventDefault()
        $('.modal-body').text($(thisObj).text())
        $.ajax({
            url: url,
            method: 'GET',
            success: function(data){
                console.log('succes')
                $('.modal-body .modal-body-inner').html(data.form)
                $('.modal-btn').click()
            },
            error: function (errorData){
                console.log('error')
                console.log(errorData)
            }
        })
    }

    // register button
    let registerButton = $('.authentication .register')
    registerButton.click(function (event){
        registerLogin(event, this, '/register/')
    })

    let loginButton = $('.authentication .login')
    loginButton.click(function (event){
        registerLogin(event, this, '/login/')
    })

    // logout button
    let logoutButton = $('.authentication .logout')
    logoutButton.click(function(event){
        event.preventDefault();
        $.ajax({
            url: '/logout/',
            method: 'GET',
            success: function (data){
                console.log('success logout')
                $('.modal-body .close').click()
                logoutButton.addClass('d-none')
                $('.authentication .account').addClass('d-none')
                authButton.removeClass('d-none')
            },
            error: function (errorData){
                console.log('error')
            }
        })
    })

    //account-page


})
