class MyComponent extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `<h1>Hello world</h1>`;
  }
}
    
customElements.define('my-component', MyComponent);

console.log('Hello world')
const shadowRoot = document.getElementById('example').attachShadow({ mode: 'open' });
console.log(shadowRoot)
shadowRoot.innerHTML = `<style>
                          button {
                            color: tomato;
                          }
                          </style>
        <button id="button">This will use the CSS color tomato <slot></slot></button>`;

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
  get_books_call().then(b => console.log(b));
}

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
