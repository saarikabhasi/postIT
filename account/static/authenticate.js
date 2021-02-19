function showCurrentValue(element){

    //show password 
    if  (element.type == "text"){
        element.type = "password"
    }
    else{
        element.type = "text"
    }

}

function addcolors(to_type,element){

    if (to_type == "success"){
        element.classList.remove("text-danger")
        element.classList.add("text-success")
    }
    if (to_type == "danger"){
        element.classList.remove("text-success")
        element.classList.add("text-danger")
    }
}

function similaritycheck(element){
    //UserAttributeSimilarityValidator: Password should not match username and email
    var username = document.querySelector(`input[name=username]`)
    let username_value = username.value.toLowerCase()

    var email =  document.querySelector(`input[name=email]`)
    let email_value = email.value.toLowerCase()

    var similarity = document.getElementById("UserAttributeSimilarityValidator")
    
    var value = element.value.toLowerCase()

    if (username_value.includes(value) == false & email_value.includes(value) == false){ 

        addcolors("success",similarity)
    }
    else{
        addcolors("danger",similarity)
    }

}
function minimumlengthcheck(element){
    // MinimumLengthValidator: Password minimum length is 8
    var minimum_length = document.getElementById("MinimumLengthValidator")
    var value = element.value
    if (value.length >= 8){
        addcolors("success",minimum_length)
    }
    else{
        addcolors("danger",minimum_length)
    }
   
}


function numericpasswordcheck(element){
    // NumericPasswordValidator:Password must not contain only (0-9) numbers
    var numeric = document.getElementById("NumericPasswordValidator")
    var value = element.value
    const re = /^[\d]*$/
    if (!re.test(value)){

        addcolors("success",numeric)
    }
    else{
        addcolors("danger",numeric)
    }
}

function numbercheck(element){
    // NumericPasswordValidator:Password numbers (0-9) length is atleast 3
    var number = document.getElementById("NumberValidator")
    var value = element.value
    const re = /[\d]{3}/
    if (re.test(value)){
        addcolors("success",number)
    }
    else{
        addcolors("danger",number)
    }
}

function confirmpassword(element){
    // confirmValidator - Confirm both passwords are same
    var confirm= document.getElementById("confirmValidator")
    var value = element.value
    if (element.id == "password1")
    {
        var password2 = document.getElementById("password2")
        if (value == password2.value){
            addcolors("success",confirm)
        }
        else{
            addcolors("danger",confirm)
        }
    }
    else{
        if (element.id == "password2"){
            var password1 = document.getElementById("password1")
            if (value == password1.value){
                addcolors("success",confirm)
            }
            else{
                addcolors("danger",confirm)
            }  
        }
    }

    

    
   
}

function validatepassword(element){

    
    similaritycheck(element);
    minimumlengthcheck(element);
    numbercheck(element);
    numericpasswordcheck(element);
    confirmpassword(element)
    

}


