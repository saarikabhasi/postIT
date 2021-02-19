const section_list_Customer= ["new-job","ads","appointments","reviews","given_reviews"]
const section_list_Technician= ["job_requests","appointments","reviews","given_reviews"]
window.onpopstate = function(event) {   
    showSection(event.state.section);
}


async function fetch_api(url){
    const response = await fetch(url)
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    } else {
        return await response.text()
      }
}
function create_div_appointments(newvalue,display){
    for (i in newvalue){
        let value = newvalue[i]
        let main = createElement('div',null,`section-job-${value['id']}`)
        //job title
        let h1_title = createElement('h1',"mb-1  pb-3",'title',null)
        let heading = value["Job_type"]
        let a = createAnchor(null,null,null,null,`${heading[0].toUpperCase()}${heading.slice(1).toLowerCase()}`)
        a.setAttribute("href",`/advertisement/appointment/${value['id']}`)
        appendChild(h1_title,a)
        appendChild(main,h1_title)
        //schedule date and time
        let h1_datetime = createElement('h1',"m-0 p-0",'scheduled-date-time',"Job created Date & time:")
        let span_datetime =  createElement('span',null,'scheduled-date-time',null)
        let p_datetime = createElement('p',null,null,value['Date']+' on '+value['Time'])
        appendChild(h1_datetime,p_datetime)
        appendChild(h1_datetime,span_datetime)
        appendChild(main,h1_datetime)
        //job- status 
        let h1_status = createElement('h1',null,'status',"Status:")
        let span_status =  createElement('span',null,'status',null)
        let p_status = createElement('p',null,null,value['Status'])
        appendChild(span_status,p_status)
        appendChild(h1_status,span_status)
        appendChild(main,h1_status)
        let hr =createElement('hr',null,null,null)


   
        appendChild(display,main,hr)
    }
    return display
}
function create_div_ads(newvalue,display){
    for (i in newvalue){
        let value = newvalue[i]
    
        let main = createElement('div',null,`section-job-${value['id']}`)
        //job title
        let h1_title = createElement('h1',"mb-1  pb-3",'title',null)
        let heading = value["Job_type"]
        let a = createAnchor(null,null,null,null,`${heading[0].toUpperCase()}${heading.slice(1).toLowerCase()}`)
        a.setAttribute("href",`/advertisement/job-profile/${value['Job_type']}-${value['id']}`)
        appendChild(h1_title,a)
        appendChild(main,h1_title)
        //requested date and time
        let h1_datetime = createElement('h1',"m-0 p-0",'requested-date-time',"Date & time:")
        let span_datetime =  createElement('span',null,'requested-date-time',null)
        let p_datetime = createElement('p',null,null,value['Date']+' on '+value['Time'])
        appendChild(h1_datetime,p_datetime)
        appendChild(h1_datetime,span_datetime)
        appendChild(main,h1_datetime)
        //job- status 
        let h1_status = createElement('h1',null,'status',"Status:")
        let span_status =  createElement('span',null,'status',null)
        let p_status = createElement('p',null,null,value['Status'])
        appendChild(span_status,p_status)
        appendChild(h1_status,span_status)
        appendChild(main,h1_status)
        let hr =createElement('hr',null,null,null)
        appendChild(display,main,hr)
    }
    return display
}

function create_div_request(){

}

function create_div_reviews(newvalue,display){
    //received reviews
    for (i in newvalue){
        let value = newvalue[i]
        var string = ""
        let main = createElement('div',null,`section-job-${value['id']}`)
        let comment = createElement('p',null,null,value["Comment"])
        let rating  = createElement('p',null,null,null)
        for (i=1;i<=value["Rating"];i++){
            string += '<i class="fa fa-star"  style="color: #ff414e"></i>'
        }
        let diff = Math.round(value["Rating"])-value["Rating"]
        if (diff == 0.5){
            string += '<i class="fa fa-star-half" style="color: #ff414e" ></i>'
        }

        rating.innerHTML = string

        let hr =createElement('hr',null,null,null)
        appendChild(display,main,comment,rating,hr)
    }
    return display
}

function create_div_given_reviews(newvalue,display){
    for (i in newvalue){
        let value = newvalue[i]
        var string = ""
        let main = createElement('div',null,`section-job-${value['id']}`)
        let comment = createElement('p',null,null,value["Comment"])
        let rating  = createElement('p',null,null,null)

        for (i=1;i<=value["Rating"];i++){

            string += '<i class="fa fa-star"  style="color: #ff414e"></i>'
        }
        let diff = Math.round(value["Rating"])-value["Rating"]
        if (diff == 0.5){
            string += '<i class="fa fa-star-half" style="color: #ff414e" ></i>'
        }

        rating.innerHTML = string

        let hr =createElement('hr',null,null,null)
        appendChild(display,main,comment,rating,hr)
    }
    return display
}
function showSection(section){

    let lookuplist = `section_list_${user_role}`
    let url  =`section/${section}`
    const null_values = {
        "ads":"You have not posted any ads",
        "appointments":"You have no appointments",
        "reviews":"You have no reviews",
        "past_jobs":"You have no past jobs",
        "given_reviews":"You have not given any reviews",
        

    }
   
    if (eval(lookuplist).includes(section)){
        // section new-job is the only section where we need to fetch form 
        if (section == "new-job"){
            //Get job form 
            getAutosavedForm();
            document.querySelector("#new-job-form").classList.remove('d-none')
            document.getElementById("display").innerHTML = ""
            document.querySelectorAll(`[class*="new_job_form_components"]`).forEach(field =>{
                field.addEventListener("change",function(){
                    setAutosaveForm(this);
                });
            })
            
        }
        else{
            fetch_api(url).then((text)=>{
                var result= JSON.parse(text)

                const keys = ["result"] 
                let display = createElement('div',null,null,null);
                keys.forEach(key=>{
            
                    newvalue = result[key]

                    if (newvalue == 0){
                        
                        let p = createElement('p',"text-danger text-center",null,null_values[section])
                        appendChild(display,p)
                        document.getElementById("display").innerHTML = display.innerHTML
                    }
                    else{
                        
            
                        
                        let func = `create_div_${section}(newvalue,display)`
                        display = eval(func)
             
                        
                    }
                    document.querySelector("#new-job-form").classList.add('d-none')
                    document.getElementById("display").innerHTML = display.innerHTML
                })
        
        })
            
        }
        


        
        
        
        
    }
   
}
//autosave form when page refresh or reload
function getAutosavedForm(){


      for (field in sessionStorage){
        if (sessionStorage.getItem(field))
            if( document.querySelector(`[name*="${field}"]`) ){
            //field exists in session storage and in form
            //get saved values
            document.querySelector(`[name*="${field}"]`).value = sessionStorage.getItem(field);
        }
    }

}
function setAutosaveForm(e){
    //save values to sessionStorage
    sessionStorage.setItem(e.name, e.value);
    
}
//show show based user choice (current or other saved address)
function show_address(element){

    //show address based on user selection

    // show current address -if user chooses current address
    if (element.value === "current_address"){
       
       show_current_address();
    }
     // show all other address -if user chooses another address
    if (element.value === "another_address"){
        show_another_address();
    }

}
//Show current address 
function show_current_address(){
    //create cards to display current address

     let result_display = createElement('div',null,null,null);
     //main card
     let card = createElement('div',"card card-body item card-body item p-3 m-3",null,null);
     
     // get other saved current address from server

     fetch(`section/new-job/address/`)
     .then(response => response.text())
     .then(text => {
 
         var result = JSON.parse(text);
 
         const keys = ["result"] 
 
         keys.forEach(key=>{
            
             newvalue = result[key]

             // if user has no saved current address, show add address button 
             if (!newvalue){
                 let add = createElement('a')
                 add.setAttribute("href","#display_address")
                 add.setAttribute("type","current")
                 add.innerHTML="Add address"
                 add.setAttribute("onclick",'add_new_address(this)')
                 appendChild(parent=card,add)
                 appendChild(parent=result_display,card)
             }
             else{
                 // if user has saved current address, show address in card
                 for (i in newvalue){
                 
                     result_display = create_address("current",newvalue[i],result_display)
                       
                 }
             
             }      
         })
         document.getElementById("display_address").innerHTML = result_display.innerHTML 
        
         
     })
   
 
    
 
   
 }
//Show all other saved address 
 function show_another_address(){

     //create cards to display all other saved address
 
     let result_display = createElement('div',null,null,null);
 
     // by default show add another address card
     // add another address card
     let add = createElement('a',null,"new-another-address")
     add.setAttribute("type","another")
     add.setAttribute("href","#display_address")
     add.innerHTML="Add address"
     add.setAttribute("onclick",'add_new_address(this)')
   
     //main card
     let div = createElement('div',null,null,null);
     let card=createElement('div',"card card-body item p-3 m-3",null,null);
     appendChild(parent=card,add)
     appendChild(parent=div,card)
     
     // get saved address from server
     fetch(`section/new-job/savedaddress/`)
     .then(response => response.text())
     .then(text => {
         var result = JSON.parse(text);
         const keys = ["result"]
         keys.forEach(key=>{
             newvalue = result[key]

             for (i in newvalue){
                 result_display = create_address("add",newvalue[i],result_display)
             }
         })
         
         document.getElementById("display_address").innerHTML = div.innerHTML + result_display.innerHTML
         
     })
 
 }
//set selected address in form
function setaddress(e){

    // When user chooses a address,
    //  1.put that address in text field. -used only for display
    //  2. Add the address id to Job form field 'Location'

    //get address id 
    if (e.value){
        id_lookup = `address_${e.value}`
    }

    //get the div and get address from its innerhtml
    let selected_address_card = document.getElementById(`${id_lookup}`)

    //store result in string
    let val = ""
    let list = ["p.line1","p.line2","p.city","p.state","p.country","p.zip"]

    for (i in list){
        //append the address contents to resultant string
        val += selected_address_card.querySelector(list[i]).innerHTML+","
    }

    //store selected location id to the job form field 'Location'
    document.querySelector(`[name*="Location"]`).value = e.value
    document.querySelector(`[name*="Location"]`).disabled =false

    //display selected address
    document.querySelector(`[name*="display_location"]`).value = val
   

    //remove showing all address 
    document.getElementById("display_address").innerHTML = ""

}
//address card to display address
function create_address(type,value,result_display){
    //create address card

    let card=  createElement('div',"card card-body item p-1  m-1",`address_${value["id"]}`,null);
    let p_line1 = createElement('p',"line1",null,value["Line1"])
    let p_line2 = createElement('p',"line2",null,value["Line2"])
    let p_city = createElement('p',"city",null,value["City"])
    let p_state = createElement('p',"state",null,value["State"])
    let p_country = createElement('p',"country",null,value["Country"])
    let p_zip = createElement('p',"zip",null,value["Zipcode"])
    if(type=="add"){

        var btn = createElement('span',null,null,'<button name="another-address" class ="btn btn-primary" type="submit" onclick="setaddress(this)" value='+value["id"]+'>save</button>')
    }
    if (type == "current"){
        var btn = createElement('span',null,null,'<button name="current-address" class ="btn btn-primary" type="submit" onclick="setaddress(this)" value='+value["id"]+'>save</button>')
    }
    
    appendChild(parent=card,p_line1,p_line2,p_city,p_state,p_country,p_zip,btn)
    appendChild(parent=result_display,card)
    
    
    return result_display
}
//add address
function add_address(e){

    let result_display = createElement('div',null,null,null);
    let div = createElement('div',null,null,null)

    
    const data = new URLSearchParams();

    let ele = document.getElementById("new-address-form")
    for (const el of new FormData(ele)){
        //append form values to data
        data.append(el[0],el[1])
    }
    data.append(e.name,e.value)
    //add address to server 
    fetch(`section/new-job/add-address/`, {
        method: 'post',
        body: data,
    })
    .then(response => response.text())  
    .then(text => {
        var result = JSON.parse(text);
        
        const keys = ["result"]
        keys.forEach(key=>{
            
            newvalue = result[key]
            for (i in newvalue){
                result_display = create_address("add",newvalue[i],result_display)
            }
        })
        if (e.value == "another"){
            // add new address in the order of 
            //1. add new address link card, 
            //2. newly created address
            //3. rest of all cards

            //append node 0 
            let objects= document.querySelector("#display_address").childNodes
      
            //append node 1 to div
            appendChild(parent=div,objects[0],result_display)
            for (let nodes=1;nodes<objects.length;nodes++){
                //append rest all nodes

                appendChild(parent=div,objects[nodes])
            }
            document.getElementById("display_address").innerHTML=div.innerHTML
        }
        if (e.value == "current"){
            document.getElementById("display_address").innerHTML = result_display.innerHTML
        }
        

       
        
    })

    document.getElementById("show-address-form").innerHTML=""
    document.getElementById("display_address").style.display=""
}
//add new address feature 
function add_new_address(e){
    //add new address -display address form and google automplete headers

    setup_google_autocomplete();
    let display = createElement('div',null,null,null);

    let div = createElement('div',"card card-body  item p-3 m-3","new-address",null);
    display = createFormAddress(div,null);


    let form = createForm("post",null,null,"new-address-form")
    let crsf = formCrsf();
    if(e.type=="another"){

        var submitbutton = createElement('span',null,null,'<button name="address-type" value="another" class ="btn btn-primary" type="submit" onclick="add_address(this)" >save</button>')
    }
    if (e.type == "current"){
        var submitbutton = createElement('span',null,null,'<button name="address-type" value ="current" class ="btn btn-primary" type="submit" onclick="add_address(this)">save</button>')
    }
    

    
    

    appendChild(parent=display,submitbutton)
    appendChild(parent=form,crsf,display)

    let result_div = createElement('div',null,null,null);
    appendChild(parent=result_div,form)

    document.getElementById("display_address").style.display="none"
    document.getElementById("show-address-form").innerHTML = result_div.innerHTML 
}

  window.addEventListener('load', (event) => {
    // by default show new-job form
    
     
     window.history.pushState({section:initialcategory},"",`${initialcategory}`)
     //storing previousection to localstorage so that i can use the information while refreshing the page!
     localStorage.setItem("previoussection", initialcategory);

     showSection(initialcategory);   
     
    document.querySelectorAll('#button').forEach(button =>{
        if (button.dataset.section == initialcategory){
            var current = document.getElementsByClassName("active");    
            
            current[0].classList.remove("active")
            button.classList.add("active")
        }
    })
 })
 // DOMContentLoaded page -Add button click functionality
document.addEventListener('DOMContentLoaded',function(){

    

 // Add section functionality on button click
    document.querySelectorAll('#button').forEach(button =>{
        button.onclick = function(){
            let section = this.dataset.section
            window.history.pushState({section:section},"",`${section}`);
            localStorage.setItem("previoussection", section);
            showSection(section);

            var current = document.getElementsByClassName("active");    
            current[0].classList.remove("active")
            this.classList.add("active")

        };
    
 
     
 });
});

