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
      <div class="title"><slot name="title"> </slot></div>
      <div class="author"><slot name="author"> </slot></div>
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
      const t = document.createElement('book-component');
      // const shadowRoot = t.shadowRoot
      const s = document.createElement('span');
      const s2 = document.createElement('span');
      s.innerHTML = b.name;
      s.slot = 'title'
      s2.innerHTML = b.author;
      s2.slot = 'author';
      t.appendChild(s)
      t.appendChild(s2);
      list.appendChild(t);
    })));
}

const book_template = document.createElement('template');
book_template.innerHTML = `
  <span slot="title"></span>
  <span slot="author"></span>
`
get_books();
/*
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
