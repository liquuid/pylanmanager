/**
 * @param string url - URL que processara a requisicao do cliente
 * @param string objHtmlReturn - ID do objeto HTML onde sera exibido o resultado 
 * @param int id - Valor enviado como base para obter um retorno
 */
function comboAjax(url,objHtmlReturn,id)
{
  // Cria uma variável dados em formato JSON, com 1 chave e 1 valor
  dados = {'id':id};
 
  // É inserido um elemento option dentro do elemento select
  $("#"+objHtmlReturn).html('<option value="0">Carregando...</option>');
  $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: dados,
      success: function(retorno){
          $("#"+objHtmlReturn).empty();
          $.each(retorno, function(i, item){
              $("#"+objHtmlReturn).append('<option value="'+item.pk+'">'+item.fields[fieldreturn]+'</option>'); 
 
          });
      },
      error: function(erro) {
        alert('Erro. Sem retorno da requisicao.');
      }
  });
}
function Editar(urlprocess,objForm,objSelect)
{ 
  var id = $('#'+objSelect+' option:selected').val();
  if ((id > 0) && (id != '')) {
    $('#'+objForm).attr('action',urlprocess);
    $('#'+objForm).submit();
  } else
    alert('Selecione um item primeiro.');
}
 
function Excluir(urlprocess,objForm,objSelect)
{ 
  if (confirm('Tem certeza?'))
    Editar(urlprocess,objForm,objSelect)
}
