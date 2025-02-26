document.addEventListener('DOMContentLoaded', function () {
    // the form in which the question are placed
    const questionContainer = document.querySelector(".question")
    
    // form to take enquiries for asking questions
    let questionForm = document.querySelector(".ask_question")

    // the main div in which the question are placed
    let questionToSubmit_div = document.querySelector(".question_to_submit")
    questionToSubmit_div.style.display = "none" 
    
    questionForm.addEventListener('submit', function (event) {
        event.preventDefault()
        let numOfquestion = document.querySelector(".numberOfquestion").value
        let numOfoption = document.querySelector(".numOfoption").value
        allQuestions = document.createElement("div")

        for (let i = 0; i < numOfquestion; i++){
        // each question is wrapped in a the div
        let questionNum = document.createElement("div")
        questionNum.style.padding = "15px 0";
        let questionlabel = document.createElement("label")
        questionlabel.textContent = `${i + 1}-`
        questionNum.appendChild(questionlabel)
        questionNum.classList.add("col-12")
        // an input to store the question 
        let question = document.createElement("input")
        let j = 0
        question.setAttribute("type", "text")
        question.classList.add("form-contol")
        question.classList.add(`question${i + 1}`)
        
        questionNum.appendChild(question)
        let div = document.createElement("div")
        div.style.padding = "14px 0 7px 0";
        let optionLable = document.createElement("label")
        optionLable.textContent = (String.fromCharCode(97+j)+ "-")
        let answer = document.createElement("input")
        let answer_explain = document.createElement("input")
        answer.style.padding = "7px 0"
        answer.setAttribute("type", "radio")
        answer.setAttribute("name", `option${j+1}`)
        answer.classList.add("oui")
            
        let label = document.createElement("input")
        label.setAttribute("type", "text")
        label.setAttribute("placeholder", "The answer here")
        // answer_explain.setAttribute("type", "text")
        answer_explain.setAttribute("placeholder", "Explain the answer here")
        answer_explain.classList.add("answer_explain")
        answer_explain.style.margin = "7px 0 7px 50px";
        div.appendChild(optionLable)
        div.appendChild(answer)
        
        div.appendChild(label)
        questionNum.appendChild(div)
        questionNum.appendChild(answer_explain)
    
            for (j = 1; j < numOfoption; j++){
            let div = document.createElement("div")
            let option = document.createElement("input")
            let optionLable = document.createElement("label")
            optionLable.textContent = (String.fromCharCode(97+j)+ "-")
            div.style.padding = "7px 0";
            option.setAttribute("type", "radio")
            option.setAttribute("name", `option${i+1}`)
            option.classList.add("option")
                
            let label = document.createElement("input")
            label.setAttribute("placeholder", "Option here")
            div.appendChild(optionLable)
            div.appendChild(option)
            div.appendChild(label)
            questionNum.appendChild(div)
                
            questionForm.style.display = "none"
            allQuestions.appendChild(questionNum)
            questionToSubmit_div.style.display = "" 
    }
            questionContainer.style.display = "block"
            questionContainer.appendChild(allQuestions) 
    }
    })
   

    

})