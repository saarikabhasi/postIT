
async function schedule_appointment(e){

    const response = await fetch(`/advertisement/schedule-appointment/${e.value}`) 
    
    if (response.ok){
        // create modal
        const text = await response.text()   
        let result = JSON.parse(text)

        let date = new Date (result["Date"][0]["Date"])
        let date_string = date.toDateString()

        let time = result["Time"][0]["Time"]
        time_string = time.toString().slice(0,2)

        let time_int = parseInt(time)
        if (time_int<12){
            time = time + " AM"
        }
        if (time_int >= 12){
            time = time + " PM"
        }

        let modal_dialog = createElement('div',"modal-dialog")
        let  modal_content = createElement('div','modal-content')

        
        let  modal_header = createElement('div','modal-header')
        let h5 = createElement('h5','modal-title',null,'Your appointment created!')
        let closebtn = createButton('button',null," btn close-btn",null,null,'&times;')
        closebtn.setAttribute('data-bs-dismis','modal')
        closebtn.setAttribute('aria-label',"Close")

        closebtn.setAttribute("onclick",'hide()')
        appendChild(modal_header,h5,closebtn)

        let modal_body = createElement('div',"modal-body",null,null)
        let p_date = createElement('p',null,null,"Event Date: "+date_string)
        let p_time = createElement('p',null,null,"Event Time: "+time)
        let p_amount = createElement('p',null,null,"Amount: "+result["Amount"][0]["Amount"]+' '+result["Currency"][0]["Currency"])
        appendChild(modal_body,p_date,p_time,p_amount)
        
        let modal_footer = createElement('div',"model_footer",null,null)

        let apptbtn = createAnchor(null,'btn',null,null,'see your appointment')
        apptbtn.setAttribute('href',`/advertisement/appointment/${result["Job_id"]}`)
        appendChild(modal_footer,apptbtn)
        appendChild(modal_content,modal_header,modal_body,modal_footer)
        appendChild(modal_dialog,modal_content)
        let obj =document.querySelector("#display-modal")
        obj.append(modal_dialog)
        obj.style.display = "block"
    

        
    }
    

}
function hide(){
    let obj =document.querySelector("#display-modal")
    obj.style.display = 'none'
    location.reload();

}

