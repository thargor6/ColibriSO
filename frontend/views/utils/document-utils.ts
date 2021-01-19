export const selectElementFromComponent = (webComponent: string, selector: string) => {
  return document.querySelector(webComponent)!.shadowRoot!.querySelector(selector);
}