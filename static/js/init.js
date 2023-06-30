let modelReady = false


window.onload = () => {
    fetch('/load_data', {
        method: 'GET'
    }).then((r) => {
        if (r.status === 200) {
            modelReady = true
        }
    })
}