$(() => {
    main()
    $(window).resize(main)
})

function main() {
    pushBottom()
}

function pushBottom() {
    $('.push-bottom').each(function() {
        const $elem = $(this)

        console.log('\n\nelem:')
        console.log($elem)

        let sibHeights = 0
        $elem.siblings().each(function() {
            const sibHeight = parseInt($(this).outerHeight(true))

            console.log('\tsib: ')
            console.log($(this))
            console.log('\t\tsibHeight: ' + sibHeight)

            sibHeights += sibHeight
        })
        
        $elem.css('margin-top', 'auto')
        const elemMarginTop = parseInt($elem.css('margin-top'))
        const elemFullHeight = parseInt($elem.outerHeight(true))
        const parHeight = parseInt($elem.parent().height())
        const resultMargin = parHeight - sibHeights - elemFullHeight + elemMarginTop


        console.log('elemMarginTop: ' + elemMarginTop + '\nelemFullHeight: ' + elemFullHeight + '\nparHeight: ' + parHeight)
        console.log('result margin: ' + resultMargin + 'px')
        $elem.css('margin-top', resultMargin + 'px')
    })
}

function eventFire(el, etype) {
    if (el.fireEvent) {
      el.fireEvent('on' + etype)
    } else {
      let evObj = document.createEvent('Events')
      evObj.initEvent(etype, true, false)
      el.dispatchEvent(evObj)
    }
  }