
export const switchTheme = (newTheme: string) => {
    const body: HTMLElement = document.querySelector("body")!;
    body.attributes.getNamedItem('theme')!.value = newTheme;
}
