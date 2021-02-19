// header file used by other javascript file
function formCrsf(){
    //csrf
    var crsf = document.createElement("input");
    crsf.setAttribute("type","hidden");
    crsf.setAttribute("name","csrfmiddlewaretoken");
    crsf.setAttribute("value",csrfToken);
    

    return crsf
}

function createElement(tag,className,idName,content){
    //createElement
    element = document.createElement(tag);

    if (className){element.className = className;}
    if (idName){element.id = idName;}
    if (content){element.innerHTML = content;}
    
    return element;

}

function createForm(method,action,onsubmit,id){
    //form

    element = document.createElement("form");
    if (method){element.setAttribute('method',method);}
    if (action){element.setAttribute('action',action);}
    if (onsubmit){element.setAttribute('onsubmit',onsubmit);}
    if (id) {element.setAttribute('id',id)}
  

    return element
}

function createButton(type,idName,className,name,value,content){
    //button

    element = document.createElement("button")
    if (type){element.type = type;}
    if (className){element.className = className;}
    if (idName){element.id = idName;}
    if (name){element.name = name;}
    if (value){element.value = value;}
    if (content){element.innerHTML = content;}

    return element
}

function createTextarea(rows,cols,id,name,content,form,required){
    //textarea
    element = document.createElement("textarea")
    if (rows){element.rows = rows;}
    if (cols){element.cols = cols;}
    if (id){element.id = id;}
    if (name){element.name = name;}
    if (form){element.form = form;}
    if (content){element.innerHTML = content;}
    if (form){element.form = form;}
    if (required){element.required = true;}
    return element
}
function appendChild(parent,...args){
    //appendchild
    for (let i =0 ;i<args.length;i++){
        parent.appendChild(args[i]); 
    }
 
    return parent
}

function createInput(idName,className,type,name,placeholder){
    //csrf
    var input = document.createElement("input");
    input.type = type;
    input.name = name;
    input.placeholder = placeholder;
    if (className){input.className = className;}
    if (idName){input.id=idName;}

    // input.autofocus='';
    
    return input
}

function createLabel(content,name,className,idName){
    var label = document.createElement("label");
    label.innerHTML = content;
    label.name = name;
    label.className =className
    label.idName = idName
    return label
}
function createSelect(name,idName){
    var select = document.createElement("select");

    select.name = name;

    select.idName = idName
    return select
}
function createOption(value,content){
    var option = document.createElement("option");
    option.value= value;
    option.innerHTML = content
    return option
}


function createAnchor(idName,className,name,type,content){
    element = document.createElement("a")
    if (idName){element.id = idName;}
    if (className){element.className = className;}
    if (name){element.name = name;}
    if (type){element.type = type;}
    if (content){element.innerHTML = content;}

    return element
}

