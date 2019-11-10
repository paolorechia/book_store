'use strict';
class BookComponent extends HTMLElement {
  static get observedAttributes() {
    return [];
  }
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  attributeChangedCallback(attrName, oldValue, newValue) {
    if (oldValue !== newValue) {
      this[attrName] = this.hasAttribute(attrName);
    }
  }
  connectedCallback() {
    const { shadowRoot } = this;
    shadowRoot.innerHTML = `
      <div class="title"><slot> </slot></div>
      <div class="author"><slot> </slot></div>
    `
  }
}
customElements.define('book-component', BookComponent);

var myHeaders = new Headers();
myHeaders.set('Access-Control-Allow-Origin', '*');

async function get_books_call() {
  const options =  {
    method: 'GET',
    headers: myHeaders
  }
  const response = await fetch('http://localhost:4040/books')
  const data = await response.json(); 
  return data;
}

function get_books() {
  const list = document.getElementById("book-list");
  get_books_call().
    then(json_ => (json_.map(b => {
      console.log(b); 
      const t = document.createElement('book-component');
      console.log(t)
      const s = document.createElement('span');
      console.log(b.name)
      s.innerHTML = b.name;
      const s2 = document.createElement('span');
      s2.innerHTML = b.author;
      t.appendChild(s)
      t.appendChild(s2);
      list.appendChild(t);
    })));
}
get_books();

/*
        <book-component>
          <span slot="title"> Titulo </span>
          <span slot="author"> Autor </span>
        </book-component>
const fragment = document.getElementById('book-template');
const books = [
  { title: 'The Great Gatsby', author: 'F. Scott Fitzgerald' },
  { title: 'A Farewell to Arms', author: 'Ernest Hemingway' },
  { title: 'Catch 22', author: 'Joseph Heller' }
];

books.forEach(book => {
  // Create an instance of the template content
  const instance = document.importNode(fragment.content, true);
  // Add relevant content to the template
  instance.querySelector('.title').innerHTML = book.title;
  instance.querySelector('.author').innerHTML = book.author;
  // Append the instance ot the DOM
  document.getElementById('books').appendChild(instance);
;
*/
