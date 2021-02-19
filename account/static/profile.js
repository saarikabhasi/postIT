function get_previous_form_values(section){
    let element = document.querySelector(`#${section}`)
    let value ={}
    element.childNodes.forEach(e => { 
        if (e.id){
            
            value[e.id] = e.innerHTML
        }
     
    })

    return value
}


//edit profile
function edit_profile(section){
    
    idname = `${section}` 
    value = document.getElementById(idname).innerHTML

    if (form_sections.includes(section)){
        value = get_previous_form_values(section)
    }
    if (section == "Address"){
       
        setup_google_autocomplete();


        
    }

    
    display = setup_profile_edits(section,value)

   // document.getElementById(`profile_${section}`).style.display="none";
    document.getElementById(`profile_${section}`).classList.add("d-none")
    document.getElementById(`edit_${section}`).innerHTML = display.innerHTML
   
    
}
async function save_textarea(section,newvalue){
    //save text area after edit or adding new
    let  profile_section= document.querySelector(`#profile_${section}`)

    const response = await fetch(`updateprofile/${section}/${newvalue}`) 
    const text = await response.text()
    let result = JSON.parse(text)

    if (profile_section){
        //edit 
        document.getElementById(`${section}`).innerHTML= result["result"][0][`${section}`]


    }
    else{
        //create 
        let display = createElement('div')
        display = create_div_for_section_with_textareas(section,display,result["result"][0])
 
        return display
    }


}
async function save_form(section,path,data){
    // save updated form values to server 

    

    let  profile_section= document.querySelector(`#profile_${section}`)

    const response  = await fetch(path, { method: 'post', body: data,})
    const text = await response.text()

    let result = JSON.parse(text)
    if (profile_section){
        //edit
        var status= save_edited_section_to_div(section,result["result"])

    }
    else{
        //new
        let display = createElement('div')
        display= create_div_for_section_with_forms(section,display,result["result"][0])
 
        return display

        
        
       
        
    }

}


async function save_edited_section_to_div(section,newvalue){
    // save edited sections
    for (i in newvalue){
        // edit

        let element = document.querySelector(`#${section}`)
        
        element.childNodes.forEach(e => { 
            if (e.id){
               
                document.getElementById(e.id).innerHTML = newvalue[i][e.id]
            }     
        })
       
    }
  

return 1   

}
function create_div_for_section_with_textareas(section,display,newvalue){
    // create divs to show new entry for textarea

    let div_idname  =  `profile_${section}`
    let div_profile = createElement('div',"profile_form_components flex-container",div_idname,null)
    let p = createElement('p',null,`${section}`,newvalue[section])

    let span = createElement('span',null,null,null)
    let input_hidden = createInput('edit',null,null,null,null)
    input_hidden.setAttribute('type','hidden')
    input_hidden.setAttribute('value',newvalue["id"])
    let anchor = createAnchor("edit",null,"edit",'submit','<i class="fa fa-pencil" style = "color:#f7786b"></i>')
    anchor.setAttribute("onclick",`edit_profile('${section}')`)
    appendChild(span,input_hidden,anchor)
    appendChild(div_profile,p,span)
    let div_edit_section = createElement('div',"profile_edits",`edit_${section}`)
    appendChild(display,div_profile,div_edit_section)
    return display

}
async function create_div_for_section_with_forms(section,display,newvalue){
    // create divs to show new entry for forms

    let div_idname  =  `profile_${section}`
    let div_profile = createElement('div',"profile_form_components flex-container",div_idname,null)
    let div_section = createElement('div',"card-body",`${section}`,null)
    let keystoignore = ["id","User_id"]
    let keys = Object.keys(newvalue)
  
    for (k in keys){
        if (!keystoignore.includes(keys[k])) {
        
        let p = createElement('p',null,keys[k],newvalue[keys[k]])
        appendChild(parent=div_section,p)
    }
    }

    let span = createElement('span',null,null,null)
    
    let input_hidden = createInput('edit',null,null,null,null)
    input_hidden.setAttribute('type','hidden')
    input_hidden.setAttribute('value',newvalue["id"])
    // function createAnchor(idName,className,name,type,content){
    let anchor = createAnchor("edit",null,"edit",'submit','<i class="fa fa-pencil" style = "color:#f7786b"></i>')
    anchor.setAttribute("onclick",`edit_profile('${section}')`)

    let div_edit_section = createElement('div',"profile_edits",`edit_${section}`)
    appendChild(span,input_hidden,anchor)

    appendChild(div_profile,div_section,span)
    
    appendChild(display,div_profile,div_edit_section)

  
    return display
 
}
async function update_licence(e){

    let  profile_section= document.querySelector(`#profile_Licence`)
    let value = e.checked.toString()
    let newvalue = value[0].toUpperCase()+value.slice(1)
   
    const response = await fetch(`updateprofile/Licence/${newvalue}`) 
    const text = await response.text()
    
    
}
//save profile
function save_profile(section){

    var validate_res=""
    let newvalue = ""
    validate_sections = ["Fullname","Recovery_email","Phone_number","Totalexperience","About","Designation"]
    //validate values before sending to server 
    if (validate_sections.includes(section)){
       
        newvalue=validate_values(section)
        if (newvalue.length>0){
            validate_res = true
            //let path = 
        }
        if (!validate_res){
            return
        }
    }
    if (section_with_dates.includes(section)){
        if (!validateDate()){
            return 
        }
    }
    if(textarea_sections.includes(section)){
        //section with textarea 
        var display = save_textarea(section,newvalue)
        
    }
    else if(section == 'Licence'){
        update_licence(section,newvalue)
    }

    else{
        //section with form
        let path = `updateprofile/${section}`
        //generate form data from dom
        const data = new URLSearchParams();
        let ele = document.getElementById(`new-${section}-form`)
        for (const el of new FormData(ele)){
            //append form values to data
            data.append(el[0],el[1])
        }

        var display = save_form(section,path,data)

    }
    
    if (document.querySelector(`#profile_${section}`)){
    // edit    
    document.querySelector(`#edit_${section}`).innerHTML=""
    document.querySelector(`#profile_${section}`).classList.remove("d-none")    
    }
    //new
    display.then(function(result_display){
        //wait for function to be done and update those values
        if (result_display){
        document.querySelector(`#article_${section}`).innerHTML = result_display.innerHTML
        
        }
    })

 return 1   
}

//add profile
function add_new_profile(section){

    idname = `${section}` 
    let display = createElement('div',null,null,null);
    //let onclickfunc = `save_profile('${section}')`

    if (section == "Address"){
        //display form
        setup_google_autocomplete();
         
    }

    display = setup_profile_edits(section,null)
    document.getElementById(idname).innerHTML = display.innerHTML


}

window.onload=()=>{

    const headers_push_stack = []
    const headers_list = ["Account","Profile"]
    document.querySelectorAll("#header").forEach(a =>{

        a.onclick=function(){

           let section  = a.dataset.section

           
            status_list = []
            let element = document.querySelectorAll(`#${section}`)
            if (!headers_push_stack.includes(section)){
                headers_push_stack.push(section)
                
                element.forEach(ele =>{
                    ele.classList.remove("d-none")
                })
               // document.getElementById(section).classList.remove("d-none")
                
            }
            else{
                let index = headers_push_stack.indexOf(section)

                if (index>-1){
                    headers_push_stack.splice(index,1)
                }
                
                element.forEach(ele =>{
                    ele.classList.add("d-none")
                })
            }

            


            
            
            
        }
    })
    document.querySelectorAll('#button').forEach(button =>{
        button.onclick = function(){
            let section = this.dataset.section
        

            var current = document.getElementsByClassName("active");    
            
            current[0].classList.remove("active")
            this.classList.add("active")
        };
    
 
     
 });
}





