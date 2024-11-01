const formulario_produto = document.querySelector("#formulario_produto")
const nome_produto = document.querySelector("#nome_produto")
const preco = document.querySelector("#preco")
const qtde = document.querySelector("#qtde")

const estoque = JSON.parse(localStorage.getItem("banco_estoque")) || [];

formulario_produto.addEventListener("submit", (evento) =>{
    evento.preventDefault();
    const novo_produto = {
        nome: nome_produto.value,
        preco: preco.value,
        qtde: qtde.value,
    };
    estoque.push(novo_produto);
    localStorage.setItem("banco_estoque", JSON.stringify (estoque));
    console.log(estoque);
    formulario_produto.reset();
    nome_produto.focus();
});

