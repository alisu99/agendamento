const dataInput = document.getElementById("data")
const quadraSelect = document.getElementById("quadra")
const listaHorarios = document.getElementById("lista-horarios")
const confirmar = document.querySelector("#step-confirmar button")
confirmar.disabled = true

const hoje = new Date()
const limite = new Date()

limite.setDate(hoje.getDate() + 10)

function formatarData(data) {
    return data.toISOString().split("T")[0]
}

dataInput.min = formatarData(hoje)
dataInput.max = formatarData(limite)

function carregarHorarios() {
    const data = dataInput.value
    const quadra = quadraSelect.value
    if (!data || !quadra) return
    fetch(`/horarios/?data=${data}&quadra=${quadra}`)
        .then(response => response.json())
        .then(horarios => {
            listaHorarios.innerHTML = ""
            if (horarios.length === 0) {

                listaHorarios.innerHTML = "<p>Nenhum horário disponível para essa data</p>"
                return
            }
            horarios.forEach(h => {

                const label = document.createElement("label")
                label.classList.add("horario")

                label.innerHTML = `
                <input type="radio" name="horario" value="${h.id}">
                ${h.inicio} às ${h.fim}
            `
                listaHorarios.appendChild(label)

            })
            document.getElementById("step-horario").classList.remove("disabled")
            document.getElementById("step-horario").scrollIntoView({
                behavior: "smooth"
            })
            ativarEventoHorarios()
        })
}

function ativarEventoHorarios() {

    const radios = document.querySelectorAll("input[name='horario']")

    radios.forEach(r => {

        r.addEventListener("change", () => {

            const horarioTexto = r.parentElement.textContent.trim()
            const dataTexto = formatarDataBR(dataInput.value)
            const quadraTexto = quadraSelect.options[quadraSelect.selectedIndex].text

            document.getElementById("preview-data").textContent = dataTexto
            document.getElementById("preview-horario").textContent = horarioTexto
            document.getElementById("preview-quadra").textContent = quadraTexto

            confirmar.disabled = false

            document.getElementById("step-confirmar").classList.remove("disabled")

            document.getElementById("step-confirmar").scrollIntoView({
                behavior: "smooth"
            })

        })

    })

}
dataInput.addEventListener("change", () => {

    quadraSelect.disabled = false
    document.getElementById("step-quadra").classList.remove("disabled")
})
quadraSelect.addEventListener("change", carregarHorarios)


function formatarDataBR(data) {
    const d = new Date(data)

    return d.toLocaleDateString("pt-BR", {
        day: "numeric",
        month: "long",
        year: "numeric"
    })
}