const container = document.querySelector("#container");

const estoque = JSON.parse(localStorage.getItem("banco_estoque")) || [];

estoque.forEach((produto) => {
    const novo_card = document.createElement("div")
    novo_card.className = "card"
    novo_card.innerHTML = `
                    <h3>${produto.nome}</h3>
                    <p><strong>Preço:</strong>${produto.preco}</p>
                    <p><strong>Qauntidade:</strong>${produto.qtde}</p>
    `;
    container.appendChild(novo_card);
});