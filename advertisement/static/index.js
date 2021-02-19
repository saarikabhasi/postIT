function createNewcard(display,result,job_requested_ids){

    let div_card = createElement('div',"card item p-3 m-3",null,null);

    let h1 = createElement('h1',"card-title",null,null);

    let title_link = '<a href="job-profile/'+ result.Job_type+'-'+result.id+ '">'+ result.Job_type[0]+result.Job_type.slice(1).toLowerCase()+'</a>' 
    let hr =createElement('hr',null,null,null)

    h1.innerHTML = title_link
    
    let div_cardbody = createElement('div',"card-body",null,null);
    let date = new Date (result.Date)
    let date_string = date.toDateString()
    let p_date = createElement('p',null,null,"Event Date: "+date_string)
    let p_priority = createElement('p',null,null,"Priority: "+result.Priority)
    let p_status = createElement('p',null,null,"Status: "+result.Status)
   

    
    appendChild(parent = div_cardbody,p_date,p_priority,p_status)


    if (job_requested_ids !=null){
        if(job_requested_ids.includes(result.id)){
        let application_status = createElement('p',"text-success",null,'<i class="fa fa-check">Applied</i>')
        appendChild(parent=div_cardbody,application_status)
    }
    }
    appendChild(parent = div_card,h1,hr,div_cardbody)
    appendChild(parent = display,div_card)
    return display
    
}







window.onload = function(){

    document.querySelectorAll("#filter").forEach(input =>{
        input.onclick=function(){
            showjobsbasedfilter(input)
        }
    })


}
function showjobsbasedfilter(input){

    //display_ids =[]
    let display = createElement('div',null,null,null);
    

    fetch(`jobsearch/${input.value}`)
    .then(response => response.text())
    .then(text => {
        var result = JSON.parse(text);
        const keys = ["result"]
        keys.forEach(key=>{
            let newvalue = result[key]

            for (i in newvalue){
            
                
               
                display.innerHTML= createNewcard(display,newvalue[i],result["job_requested_ids"]).innerHTML
            }
            
            
        })

        document.getElementById("jobs").innerHTML = display.innerHTML
        
    })
}

