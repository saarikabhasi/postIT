

const textarea_sections = ["Fullname","Recovery_email","Totalexperience","Review","Phone_number","About","Designation"]
const form_sections = ["Address","Payment","Experience","Education"]
const checkbox_sections= ["Licence"]
const errors_email = {"same":"Recovery email id is same as registered email id","invalid":"Enter valid email address"}
const errors_fullname = {"invalid":"Name must be of length 1-50"}
const errors_Totalexperience = {"invalid":" Total number of experience must be number"}
const errors_phonenumber = {"invalid":"Phone number length must be between 9-15"}
const error_common = {"invalid":"Summary must be of 0-50 length"}
const section_with_dates = ["Experience","Education"]



async function setup_google_autocomplete(){
    var scriptgoogle = document.createElement("script");
    scriptgoogle.defer = true
    scriptgoogle.setAttribute("src",`https://maps.googleapis.com/maps/api/js?key=${google_key}&callback=initAutocomplete&libraries=places&v=weekly` ) 
    document.head.appendChild(scriptgoogle);
    return 1
}
    

function changecolors_textarea(section,value){
    element = document.getElementById(`textarea_${section}`)
    element.style.color = "red"
    element.style.borderColor = "red"
    element.innerHTML = value
    return element
}
function validateEmail(email,section) {
    

    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    let email_format_check = re.test(email)
    let email_id_same_as_recovery_email = (email === user_email)
  
    if (!email_format_check || email_id_same_as_recovery_email ){
        textarea = changecolors_textarea(section,email)
        if (!email_format_check){

            document.getElementById(`${section}_error`).innerHTML = errors_email["invalid"]
        }
        if (email_id_same_as_recovery_email){
            document.getElementById(`${section}_error`).innerHTML = errors_email["same"]
        }

        return false
    }
 
        
      
    return true
    
}
function validateFullname(fullname,section) {

    const re = /^[a-zA-Z0-9\x20]{1,50}$/
    if (!re.test(fullname)){
        textarea = changecolors_textarea(section,fullname)
        document.getElementById(`${section}_error`).innerHTML = errors_fullname["invalid"]
      
        return false
    }
 
    return true
    
}
function validateAbout_Desgination(value,section) {

    const re = /^[a-zA-Z0-9\x20]{1,50}$/
    if (!re.test(value)){
        textarea = changecolors_textarea(section,value)
        
        document.getElementById(`${section}_error`).innerHTML = error_common["invalid"]
      
        return false
    }
 
    return true
    
}
function validateDate(){

    let startdate =new Date(document.getElementById("start_date").value)
    let enddate =new Date(document.getElementById("end_date").value)
    let time_diff = enddate.getTime()- startdate.getTime()
    

    if(time_diff>0){
        return true
     }else{
        document.getElementById("start_date").style.color = "red";
        document.getElementById("start_date").style.borderColor = "red";
        document.getElementById("end_date").style.color = "red";
        document.getElementById("end_date").style.borderColor = "red";

        return false
     }
}

function validateTotalexperience(experiencenumber,section){

    const re = /^[0-9]*$/
    if (!re.test(experiencenumber)){
        textarea = changecolors_textarea(section,experiencenumber)
        document.getElementById(`${section}_error`).innerHTML = errors_Totalexperience["invalid"]
      
        return false
    }
    return true
}

function validatePhonenumber(phonenumber,section){

    const re = /^\+?1?\d{9,15}$/
    if (!re.test(phonenumber)){
        textarea = changecolors_textarea(section,phonenumber)
        document.getElementById(`${section}_error`).innerHTML = errors_phonenumber["invalid"]
      
        return false
    }
    return true
}

function validate_values(section){

    let textarea = document.getElementById(`textarea_${section}`)
    const newvalue = textarea.value

    //validate fullname
    if (section == "Fullname" ){
        if(!validateFullname(newvalue,section)){
            return ""
        }
    }
    //validate recovery email
    if (section == "Recovery_email"){
        if (!validateEmail(newvalue,section)){
            return ""
        }
    }
    //validate Total years of experience
    if (section == "Totalexperience"){
        if(!validateTotalexperience(newvalue,section)){
            return ""
        }
    }

    //validate Phone number
    if (section =="Phone_number"){
        if (!validatePhonenumber(newvalue,section)){
            return ""
       }
    }
    //validate Phone number
    if (section =="About" | section =="Designation"){
        if (!validateAbout_Desgination(newvalue,section)){
            return ""
        }
    }

    //remove textarea before displaying new change
    textarea.remove()


    return newvalue

}

function createFormAddress(div,values){
   

    //Create Address form
    //line1
    let label_route= createLabel(content ="Address line1",name="ADDRESS_LINE_1", className = "profile_form_components")
    let input_route = createInput(idName ="autocomplete",className="route",type="text",name="ADDRESS_LINE_1",placeholder ="Enter address line 1")
    input_route.setAttribute("autocomplete","street-address")
    input_route.setAttribute("id","autocomplete")
    // input_route.setAttribute("onFocus","geolocate()")
    input_route.setAttribute("aria-autocomplete","list")
    // input_route.setAttribute("data-was-visible","true")

    //line2
    let label_line2 = createLabel(content ="Address line 2",name="sublocality_level_2",className = "profile_form_components")
    let input_line2 = createInput(idName ="sublocality_level_2",className="",type="text",name="sublocality_level_2",placeholder ="Enter address line 2")
    input_line2.setAttribute("autocomplete","address-level1")

    //City
    let label_locality = createLabel(content ="City",name="locality",className = "profile_form_components")
    let input_locality = createInput(idName ="locality",className="",type="text",name="locality",placeholder ="Enter city")
     input_locality.setAttribute("autocomplete","address-level2")
    
    //State
    let label_region= createLabel(content ="State",name="administrative_area_level_1",className = "profile_form_components")
    let input_region = createInput(idName ="administrative_area_level_1",className="",type="text",name="administrative_area_level_1",placeholder ="Enter state")
     input_region.setAttribute("autocomplete","address-level1")
  
    //country
    let label_country= createLabel(content ="Country",name="country",className = "profile_form_components")
    let input_country = createInput(idName ="country",className="",type="text",name="country",placeholder ="Enter country")
     input_country.setAttribute("autocomplete","address-level2")
     
    //Zip 
    let label_postal_code = createLabel(content ="Zip",name="postal_code",className = "profile_form_components")
    let input_postal_code = createInput(idName ="postal_code",className="",type="text",name="postal_code",placeholder ="Enter zip code")
     
    
     if (values){
        input_route.setAttribute("value",values["Line1"] )
        input_line2.setAttribute("value",values["Line2"] )
        input_locality.setAttribute("value",values["City"] )
        input_region.setAttribute("value",values["State"] )
        input_country.setAttribute("value",values["Country"] )
        input_postal_code.setAttribute("value",values["Zipcode"])
    }

    appendChild(parent=div,label_route,input_route,label_line2,input_line2,label_locality,input_locality,label_region,input_region,label_country,input_country,label_postal_code,input_postal_code)       

    return div

}

function createFormExperience(div,values){

   
   let label_title= createLabel(content ="Title",name="title", className = "profile_form_components")
   let input_title = createInput(idName ="title",null,type="text",name="title",placeholder ="Enter Title (Ex:Technician)")
    
   let label_employment_type= createLabel(content ="Type",name="employment_type", className = "profile_form_components")
   label_employment_type.setAttribute("for","employment_type")
   let select_employment_type = createSelect(name="employment_type",idName="Employment_type")
   let option_Full =createOption(value="Full Time",content="Full Time")
   let option_Part =createOption(value="Part Time",content="Part Time")
    
   let label_company= createLabel(content ="Company",name="company", className = "profile_form_components")
   let input_company = createInput(idName ="company",null,type="text",name="company",placeholder ="Enter Company name")
    
   let label_startdate= createLabel(content ="Start Date",name="start_date", className = "profile_form_components")
   let input_startdate = createInput(idName ="start_date",null,type="date",name="start_date",placeholder ="Enter start date")
    
   let label_enddate= createLabel(content ="End Date",name="end_date", className = "profile_form_components")
   let input_enddate = createInput(idName ="end_date",null,type="date",name="end_date",placeholder ="Enter end date")

    if (values){
    
        input_title.setAttribute("value",values["Title"] )

        if(values["Employment_type"]){
            if (values["Employment_type"] == "Full Time"){
                option_Full.setAttribute("selected",true)
            }
            if (values["Employment_type"] == "Part Time"){
                option_Part.setAttribute("selected",true)
            }
            
        }
        
        input_company.setAttribute("value",values["Company"] )
        input_startdate.setAttribute("value",values["Startdate"])
        input_enddate.setAttribute("value",values["Enddate"])
    }
   
    appendChild(parent=select_employment_type,option_Full,option_Part)  
    appendChild(parent=div,label_title,input_title,label_employment_type,select_employment_type,label_company,input_company,label_startdate,input_startdate,label_enddate,input_enddate)       
    return div
}
function createFormEducation(div,values){

   let label_school= createLabel(content ="School",name="school", className = "profile_form_components")
   let input_school = createInput(idName ="school",null,type="text",name="school",placeholder ="Enter school name")
    
   let label_degree= createLabel(content ="Degree",name="degree", className = "profile_form_components")
   let input_degree = createInput(idName ="degree",null,type="text",name="degree",placeholder ="Enter Degree")

   let label_field_of_study= createLabel(content ="Field of Study",name="field_of_study", className = "profile_form_components")
   let input_field_of_study = createInput(idName ="field_of_study",null,type="text",name="field_of_study",placeholder ="Enter Field of study")
    
   let label_startdate= createLabel(content ="Start Date",name="start_date", className = "profile_form_components")
   let input_startdate = createInput(idName ="start_date",null,type="date",name="start_date",placeholder ="Enter start date")
    
   let label_enddate= createLabel(content ="End Date",name="end_date", className = "profile_form_components")
   let input_enddate = createInput(idName ="end_date",null,type="date",name="end_date",placeholder ="Enter end date")

    if (values){

        input_school.setAttribute("value",values["School"] )

       input_degree.setAttribute("value",values["Degree"] )
       input_field_of_study.setAttribute("value",values["Field_of_study"] )
       input_startdate.setAttribute("value",values["Startdate"])
       input_enddate.setAttribute("value",values["Enddate"])
    }

    appendChild(parent=div,label_school,input_school,label_degree,input_degree,label_field_of_study,input_field_of_study,label_startdate,input_startdate,label_enddate,input_enddate)       
    return div
}
function setup_forms(section,formvalues){
    // create form for address,payment experience and education


    let onclickfunc = `save_profile('${section}')`
    let form = createForm("POST",null,null,`new-${section}-form`)
    let crsf = formCrsf();

    var submitbutton = createElement('span',null,null,'<button name="btn" class ="btn btn-primary" form = '+ `new-${section}-form` +' type="button" onclick='+onclickfunc+'>save</button>')
    let display = createElement('div',null,null,null);

    let div=  createElement('div',"card card-body col-md-11 item p-3 m-3",null,null);



    let fn = `createForm${section}(div,formvalues)`
    div = eval(fn)

    appendChild(parent = form,crsf,div,submitbutton)
    appendChild(parent = display,form)
    
   return display
}

function setup_textarea(section,onclickfunc,value){
    //textarea to edit fullname and recovery email address
    let display = createElement('div',null,null,null);

    let error_idName = `${section}_error`; 
    let textArea_idName = `textarea_${section}`
    let error_message = createElement('p','text-danger',error_idName,'')
    var textArea =  createTextarea("1","80 ",textArea_idName,`edit_${section}`,value,null)
    var submitbutton = createElement('span',null,null,'<input type= "submit" id ="saveprofile" class ="btn btn-primary" name = "btn" onclick='+onclickfunc+'>')
    
    if (!value){textArea.setAttribute("placeholder","Enter here")}
    textArea.setAttribute("autofocus",'')
    textArea.setAttribute("required",'')
    appendChild(parent = display,error_message,textArea,submitbutton)
    return display
}

function setup_profile_edits(section,value=None){

    // setup forms or textarea for editing profile

    let onclickfunc = `save_profile('${section}')`

    if (form_sections.includes(section)){

        var display = setup_forms(section,value);
 
    }
    if (textarea_sections.includes(section)){
        var display = setup_textarea(section,onclickfunc,value)
    }
    

    return display
}
