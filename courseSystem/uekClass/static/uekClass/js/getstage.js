let $=jQuery
$(function () {
    $('#id_p_id').on('change',function () {
        $.ajax({
            url:'/getstage/',
            type:'post',
            data:{'p':$(this).val()},
            success:function (e) {
                $('#id_now_stage>option').detach()
                let str=''
                str+=''
                for (i in e){
                    str+=`<option value="${i}">${e[i]}</option>`
                }
                $('#id_now_stage').html(str)
            }
        })
    })
})
// console.log($)