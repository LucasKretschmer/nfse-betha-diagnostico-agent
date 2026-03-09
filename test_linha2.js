// test_linha2.js
// Envia de forma fixa os dados da linha 2 do Excel para a API de diagnostico NFSe Betha.
// Coluna G -> erro.mensagem  |  Coluna H -> xml (JSON do sistema Betha como string)
//
// Uso: node test_linha2.js

const http = require("http");

/*const PAYLOAD = {
  xml: "{\"NFSeNumero\": \"0\", \"NFSeCodVerificacao\": \"\", \"LoteNumero\": 1004908, \"LoteCodigo\": 4909, \"LoteID_EL\": 0, \"Protocolo\": \"\", \"ChaveAcesso\": \"\", \"NFSePrefImpressao\": \"\", \"DocImpPrefeitura\": \"\", \"StatusDocumento\": 3, \"DtaHraProcessamento\": \"2026-01-20T08:24:06\", \"NFSeDataEmissao\": \"0000-00-00T00:00:00\", \"NFSeSerie\": \"\", \"DataHoraCanc\": \"0000-00-00T00:00:00\", \"EmailEnviadoEfetivado\": \"N\", \"DocStatus\": 3, \"DocStatusDescricao\": \"Rejeitado\", \"DadosRPS\": {\"ModeloDocumento\": \"NFSE\", \"Versao\": \"1.00\", \"HashRequisicao\": \"5b36343069a67145cbf27f939211b660\", \"DocIntegracao\": 1, \"RPS\": [{\"RPSNumero\": \"232388\", \"RPSSerie\": \"1\", \"RPSTipo\": \"1\", \"IDUnico\": \"\", \"dEmis\": \"2026-01-20T08:03:43\", \"dCompetencia\": \"2026-01-20T08:03:43\", \"LocalPrestServ\": \"\", \"natOp\": \"1\", \"Operacao\": \"\", \"NumProcesso\": \"\", \"benefIdNac\": \"\", \"benefNumero\": \"\", \"RegEspTrib\": \"\", \"OptSN\": \"2\", \"regApTribSN\": \"\", \"IncCult\": \"2\", \"tpImunidade\": \"\", \"tpSusp\": \"\", \"Status\": \"1\", \"cVerificaRPS\": \"\", \"EmpreitadaGlobal\": \"\", \"tpAmb\": \"1\", \"EveCodigo\": \"\", \"EveMotivo\": \"\", \"DocLegado\": \"\", \"finNFSe\": \"0\", \"indFinal\": \"1\", \"cIndOp\": \"050101\", \"tpEnteGov\": \"\", \"xTpEnteGov\": \"\", \"indDest\": \"0\", \"tpOper\": \"\", \"indDoacao\": \"\", \"NFSOutrasinformacoes\": \" Voc\u00ea pagou aproximadamente R$ 93,96 de tributos federais, R$ 0,00 de tributos estaduais, R$ 21,17 de tributos municipais, R$ 698,60 pelos produtos/servi\u00e7osFonte: IBPT A601D4\", \"cMotivoEmisTI\": \"\", \"chNFSeRej\": \"\", \"RPSCanhoto\": \"\", \"Arquivo\": \"\", \"ExtensaoArquivo\": \"\", \"RPSSubs\": {\"SubsNumero\": \"\", \"SubsSerie\": \"\", \"SubsTipo\": \"\", \"SubsNFSeNumero\": \"\", \"SubsDEmisNFSe\": \"0001-01-01T00:00:00\", \"SubsChave\": \"\", \"SubsCodMotivo\": \"\", \"SubsDescMotivo\": \"\"}, \"Prestador\": {\"CNPJ_prest\": \"SANITIZADO\", \"xNome\": \"SANITIZADO\", \"xFant\": \"SANITIZADO\", \"IM\": \"011348\", \"IE\": \"\", \"CMC\": \"\", \"CAEPF\": \"\", \"enderPrest\": {\"TPEnd\": \"PRA\u00c7A\", \"xLgr\": \"CHAMPAGNAT\", \"nro\": \"29\", \"xCpl\": \"\", \"xBairro\": \"CENTRO\", \"cMun\": \"3170701\", \"UF\": \"MG\", \"CEP\": \"37002150\", \"fone\": \"3532216626\", \"Email\": \"\"}}, \"ListaItens\": [{\"ItemSeq\": \"1\", \"ItemCod\": \"1\", \"ItemDesc\": \"\", \"ItemQtde\": \"1\", \"ItemvUnit\": \"698.6\", \"ItemuMed\": \"UN\", \"ItemvlDed\": \"0.0\", \"ItemTributavel\": \"\", \"ItemcCnae\": \"8020001\", \"ItemTributMunicipio\": \"\", \"ItemnAlvara\": \"\", \"ItemvIss\": \"0.0\", \"ItemvDesconto\": \"0.00\", \"ItemAliquota\": \"0.000000\", \"ItemVlrTotal\": \"666.11\", \"ItemBaseCalculo\": \"698.6\", \"ItemvlrISSRetido\": \"\", \"ItemIssRetido\": \"2\", \"ItemRespRetencao\": \"\", \"ItemIteListServico\": \"010301\", \"itemCodTributNacional\": \"\", \"ItemExigibilidadeISS\": \"1\", \"ItemcMunIncidencia\": \"3170701\", \"ItemNumProcesso\": \"\", \"ItemDedTipo\": \"\", \"ItemDedCPFRef\": \"\", \"ItemDedCNPJRef\": \"\", \"ItemDedNFRef\": \"\", \"ItemDedvlTotRef\": \"\", \"ItemDedPer\": \"\", \"ItemDedValor\": \"\", \"ItemVlrLiquido\": \"666.11\", \"ItemValAliqINSS\": \"0.0000\", \"ItemValINSS\": \"0.0\", \"ItemValBCINSS\": \"698.6\", \"ItemValAliqIR\": \"0.0000\", \"ItemValIR\": \"0.0\", \"ItemValBCIRRF\": \"698.6\", \"ItemValAliqCOFINS\": \"0.0300\", \"ItemValCOFINS\": \"20.96\", \"ItemValBCCOFINS\": \"0\", \"ItemValAliqCSLL\": \"0.0000\", \"ItemValCSLL\": \"6.99\", \"ItemValBCCSLL\": \"698.6\", \"ItemValAliqPIS\": \"0.6500\", \"ItemValPIS\": \"4.54\", \"ItemValBCPIS\": \"0\", \"ItemRedBC\": \"\", \"ItemRedBCRetido\": \"\", \"ItemBCRetido\": \"\", \"ItemValAliqISSRetido\": \"0.0000\", \"ItemPaisImpDevido\": \"\", \"ItemCST\": \"\", \"ItemJustDed\": \"\", \"ItemvOutrasRetencoes\": \"0.0\", \"ItemDescIncondicionado\": \"0.0\", \"ItemDescCondicionado\": \"0.00\", \"ItemTotalAproxTribServ\": \"\", \"ItemDescHospedagem\": \"\", \"ItemQtdeHospedes\": \"\", \"ItemQtdeDiariasHospedagem\": \"\", \"ItemCodQuartoHospedagem\": \"\", \"ItemDtaEntrHospedagem\": \"\", \"ItemDtaSaiHospedagem\": \"\", \"ItemValorDiariaHospedagem\": \"\", \"ItemCSTPisCofins\": \"\", \"ItemTpRetPisCofins\": \"\", \"ItemNBS\": \"115030000\"}], \"ListaParcelas\": [], \"Servico\": {\"cServ\": \"\", \"IteListServico\": \"01.03.01\", \"Cnae\": \"8020001\", \"fPagamento\": \"\", \"tpag\": \"\", \"codTributNacional\": \"\", \"TributMunicipio\": \"\", \"TributMunicDesc\": \"\", \"Discriminacao\": \"RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65!CHR13!RASTREADOR - EMPRESA N\u00c3O OPTANTE SIMPLES NACIONAL - FORA DE VGA - CSRF 4,65\", \"cMun\": \"3170701\", \"SerQuantidade\": \"\", \"SerUnidade\": \"\", \"SerNumAlvara\": \"\", \"PaiPreServico\": \"BR\", \"cMunIncidencia\": \"3170701\", \"dVencimento\": \"0001-01-01T00:00:00\", \"ObsInsPagamento\": \"\", \"ObrigoMunic\": \"\", \"TributacaoISS\": \"\", \"CodigoAtividadeEconomica\": \"\", \"ServicoViasPublicas\": \"\", \"NumeroParcelas\": \"\", \"NroOrcamento\": \"\", \"CodigoNBS\": \"115030000\", \"docRef\": \"\", \"idDocTec\": \"\", \"CST\": \"01\", \"Valores\": {\"ValServicos\": \"698.6\", \"ValPercDeducoes\": \"\", \"ValDeducoes\": \"0.0\", \"ValOutrasDeducoes\": \"\", \"ValPIS\": \"4.54\", \"ValBCPIS\": \"0\", \"ValCOFINS\": \"20.96\", \"ValBCCOFINS\": \"0\", \"ValINSS\": \"0.0\", \"ValBCINSS\": \"698.6\", \"ValIR\": \"0.0\", \"ValBCIRRF\": \"698.6\", \"ValCSLL\": \"6.99\", \"ValBCCSLL\": \"698.6\", \"RespRetencao\": \"\", \"Tributavel\": \"\", \"ValISS\": \"0.0\", \"ISSRetido\": \"2\", \"ValISSRetido\": \"\", \"ValTotal\": \"\", \"ValTotalRecebido\": \"\", \"ValBaseCalculo\": \"698.6\", \"ValOutrasRetencoes\": \"0.0\", \"ValAliqISS\": \"0.000000\", \"ValAliqPIS\": \"0.6500\", \"PISRetido\": \"\", \"ValAliqCOFINS\": \"0.0300\", \"COFINSRetido\": \"\", \"ValAliqIR\": \"0.0000\", \"IRRetido\": \"\", \"ValAliqCSLL\": \"0.0000\", \"CSLLRetido\": \"\", \"ValAliqINSS\": \"0.0000\", \"INSSRetido\": \"\", \"ValAliqCpp\": \"\", \"CppRetido\": \"\", \"ValCpp\": \"\", \"OutrasRetencoesRetido\": \"\", \"ValBCOutrasRetencoes\": \"\", \"ValAliqOutrasRetencoes\": \"\", \"ValAliqTotTributos\": \"\", \"ValLiquido\": \"666.11\", \"ValDescIncond\": \"0.0\", \"ValDescCond\": \"0.00\", \"ValAcrescimos\": \"\", \"ValAliqISSoMunic\": \"0.0000\", \"InfValPIS\": \"\", \"InfValCOFINS\": \"\", \"ValLiqFatura\": \"\", \"ValBCISSRetido\": \"\", \"NroFatura\": \"\", \"CargaTribValor\": \"\", \"CargaTribPercentual\": \"\", \"CargaTribFonte\": \"\", \"JustDed\": \"\", \"ValCredito\": \"\", \"OutrosImp\": \"\", \"ValRedBC\": \"\", \"ValRetFederais\": \"\", \"ValAproxTrib\": \"\", \"NroDeducao\": \"\", \"mdPrestacao\": \"\", \"vincPrest\": \"\", \"tpMoeda\": \"\", \"ValServEst\": \"\", \"mecAFComexP\": \"\", \"mecAFComexT\": \"\", \"movTempBens\": \"\", \"nDI\": \"\", \"nRE\": \"\", \"mdic\": \"\", \"vRecebInterm\": \"\", \"ValRedBenef\": \"\", \"PercRedBenef\": \"\", \"ValRetEstaduais\": \"\", \"ValRetMunicipais\": \"\", \"ValAliqRetFederais\": \"\", \"ValAliqRetEstaduais\": \"\", \"ValAliqRetMunicipais\": \"\", \"ValAproxTribAliqSN\": \"\", \"IBSCBS\": {\"ValTotNF\": \"\", \"ValBCIBSCBS\": \"\", \"ValCalcReeRepRes\": \"\", \"ValpRedutor\": \"\", \"ValMulta\": \"\", \"ValJuros\": \"\", \"ValInicialCobrado\": \"\", \"ValFinalCobrado\": \"\", \"ValIPI\": \"\", \"TribRegular\": {\"ValpAliqEfeRegIBSUF\": \"\", \"ValTribRegIBSUF\": \"\", \"ValpAliqEfeRegIBSMun\": \"\", \"ValTribRegIBSMun\": \"\", \"ValpAliqEfeRegCBS\": \"\", \"ValTribRegCBS\": \"\"}, \"TribCompraGov\": {\"ValpIBSUF\": \"\", \"ValIBSUF\": \"\", \"ValpIBSMun\": \"0.00\", \"ValIBSMun\": \"\", \"ValpCBS\": \"\", \"ValCBS\": \"\"}, \"IBS\": {\"ValIBSTot\": \"\", \"ValCredPresIBS\": \"\", \"ValpCredPresIBS\": \"\", \"ValIBSUF\": \"0.70\", \"ValpIBSUF\": \"0.10\", \"ValDifUF\": \"\", \"ValpDifUF\": \"\", \"ValTribOpUF\": \"\", \"ValpRedAliqUF\": \"\", \"ValpAliqEfetUF\": \"\", \"ValIBSMun\": \"0.00\", \"ValDifMun\": \"\", \"ValpDifMun\": \"\", \"ValDevTribMunIBS\": \"\", \"ValTribOpMun\": \"\", \"ValpAliqEfetMun\": \"\", \"ValpRedAliqMun\": \"\", \"ValpIBSMun\": \"\", \"ValIBSEstCred\": \"\"}, \"CBS\": {\"ValCBS\": \"6.29\", \"ValpCBS\": \"0.90\", \"ValCredPresCBS\": \"\", \"ValpCredPresCBS\": \"\", \"ValDifCBS\": \"\", \"ValpDifCBS\": \"\", \"ValpAliqEfetCBS\": \"\", \"ValpRedAliqCBS\": \"\", \"ValCBSEstCred\": \"\"}}}, \"LocalPrestacao\": {\"SerEndTpLgr\": \"\", \"SerEndLgr\": \"\", \"SerEndNumero\": \"\", \"SerEndComplemento\": \"\", \"SerEndBairro\": \"\", \"SerEndxMun\": \"\", \"SerEndcMun\": \"3170701\", \"SerEndCep\": \"\", \"SerEndSiglaUF\": \"\"}, \"IBSCBS\": {\"cLocalidadeIncid\": \"\", \"xLocalidadeIncid\": \"\", \"CSTIBSCBS\": \"000\", \"cClassTrib\": \"000001\", \"cCredPres\": \"\", \"Onerosidade\": \"\", \"PagParceladoAntecipado\": \"\", \"NCM\": \"\", \"indCompGov\": \"\", \"TribRegular\": {\"CSTReg\": \"\", \"cClassTribReg\": \"\"}}}, \"Tomador\": {\"TomaCNPJ\": \"SANITIZADO\", \"TomaCPF\": \"SANITIZADO\", \"TomaIE\": \"\", \"TomaIM\": \"\", \"TomaRazaoSocial\": \"SANITIZADO\", \"TomatpLgr\": \"\", \"TomaEndereco\": \"Avenida Jovino Fernandes Salles - de 550 a 698 - lado par\", \"TomaNumero\": \"734\", \"TomaComplemento\": \"\", \"TomaBairro\": \"Jardim Boa Esperan\u00e7a\", \"TomacMun\": \"3101607\", \"TomaxMun\": \"Alfenas\", \"TomaUF\": \"MG\", \"TomaPais\": \"BR\", \"TomaCEP\": \"37130000\", \"TomaTelefone\": \"35999011156\", \"TomaTipoTelefone\": \"\", \"TomaEmail\": \"SANITIZADO\", \"TomaSite\": \"\", \"TomaIME\": \"\", \"TomaSituacaoEspecial\": \"\", \"DocTomadorEstrangeiro\": \"\", \"TomaRegEspTrib\": \"\", \"TomaCadastroMunicipio\": \"\", \"TomaOrgaoPublico\": \"\", \"TomaEnderecoInformado\": \"\", \"TomaCAEPF\": \"\", \"TomaExSemNIF\": \"\"}, \"IntermServico\": {\"IntermRazaoSocial\": \"SANITIZADO\", \"IntermCNPJ\": \"SANITIZADO\", \"IntermCPF\": \"SANITIZADO\", \"IntermNIF\": \"\", \"IntermExSemNIF\": \"\", \"IntermIM\": \"\", \"IntermEmail\": \"SANITIZADO\", \"IntermEndereco\": \"\", \"IntermNumero\": \"\", \"IntermComplemento\": \"\", \"IntermBairro\": \"\", \"IntermCep\": \"\", \"IntermCmun\": \"\", \"IntermXmun\": \"\", \"IntermFone\": \"\", \"IntermIE\": \"\", \"IntermPais\": \"\", \"IntermUF\": \"\", \"IntermCAEPF\": \"\"}, \"ConstCivil\": {\"CodObra\": \"\", \"Art\": \"\", \"ObraLog\": \"\", \"ObraCompl\": \"\", \"ObraNumero\": \"\", \"ObraBairro\": \"\", \"ObraCEP\": \"\", \"ObraMun\": \"\", \"ObraUF\": \"\", \"ObraPais\": \"\", \"ObraCEI\": \"\", \"ObraMatricula\": \"\", \"ObraValRedBC\": \"\", \"ObraTipo\": \"\", \"ObraNomeFornecedor\": \"\", \"ObraNumeroNF\": \"\", \"ObraDataNF\": \"0001-01-01T00:00:00\", \"ObraNumEncapsulamento\": \"\", \"AbatimentoMateriais\": \"\", \"ObraXMun\": \"\", \"ObraDesc\": \"\", \"ObraCIB\": \"\", \"ObraInscImobFis\": \"\", \"ObraCPFNF\": \"\", \"ObraCNPJNF\": \"\", \"ListaMaterial\": []}, \"ListaDed\": [], \"Transportadora\": {\"TraNome\": \"\", \"TraCPFCNPJ\": \"\", \"TraIE\": \"\", \"TraPlaca\": \"\", \"TraEnd\": \"\", \"TraMun\": \"\", \"TraUF\": \"\", \"TraPais\": \"\", \"TraTipoFrete\": \"\"}, \"Locacao\": {\"categServ\": \"\", \"objetoLocacao\": \"\", \"extensaoFerrovia\": \"\", \"nPostes\": \"\"}, \"AtividadeEvento\": {\"AtivDesc\": \"\", \"AtivDataInicial\": \"\", \"AtivDataFinal\": \"\", \"AtivIdEvento\": \"\", \"AtivEndLogradouro\": \"\", \"AtivEndNumero\": \"\", \"AtivEndCompl\": \"\", \"AtivEndBairro\": \"\", \"AtivEndCEP\": \"\", \"AtivEndcMun\": \"\", \"AtivEndxMun\": \"\", \"AtivEndUf\": \"\"}, \"Pedagio\": {\"PedCategVeiculo\": \"\", \"PednEixos\": \"\", \"PedRodagem\": \"\", \"PedSentido\": \"\", \"PedPlaca\": \"\", \"PedCodAcesso\": \"\", \"PedCodContrato\": \"\"}, \"Destinatario\": {\"DestCNPJ\": \"\", \"DestCPF\": \"\", \"DestNIF\": \"\", \"DestcNaoNIF\": \"\", \"DestNome\": \"\", \"DestEndereco\": \"\", \"DestNumero\": \"\", \"DestComplemento\": \"\", \"DestBairro\": \"\", \"DestFone\": \"\", \"DestEmail\": \"\", \"DestcMun\": \"\", \"DestxMun\": \"\", \"DestCEP\": \"\", \"DestPais\": \"\", \"DestEstProvReg\": \"\"}, \"Imovel\": {\"ImovInscImobFisc\": \"\", \"ImovCIB\": \"\", \"ImovCEP\": \"\", \"ImovEndereco\": \"\", \"ImovNumero\": \"\", \"ImovComplemento\": \"\", \"ImovBairro\": \"\", \"ImovxMun\": \"\", \"ImovEstProvReg\": \"\"}, \"ListaDocumentos\": [], \"ListaNFSeReferenciadas\": [], \"ListaBensMoveis\": [], \"ListaDedIBSCBS\": [], \"ListaNFSeRefPagAntecipado\": []}]}, \"EveCodigo\": \"\", \"EveMotivo\": \"\", \"EveTp\": 0, \"GUID_Conector\": \"\", \"GUID_Instancia\": \"\", \"CocRetornoAssincronoNFSe\": false, \"NFSOutrasInformacoesRetorno\": \"\", \"EmailEnviadoCancelado\": \"N\", \"NFSeNumeroMunic\": 0, \"UltimoNSU\": \"\", \"PrcChvParceiro\": \"\", \"procNFSe\": {\"cStat\": 999, \"xMotivo\": \"Rejeitado\"}, \"Logs\": [{\"LogCodigo\": \"328\", \"LogDescricao\": \"[#inv0328] - Mensagem retornada pela prefeitura: C\u00f3digo: E001\", \"LogDtaHora\": \"2026-01-20T08:21:58\", \"LogTipo\": 1, \"LogObjeto\": \"PNFS208\", \"ExeAcao\": \"E\", \"ExeWsvServico\": 1, \"ProcessoId\": \"2026012008215786_11339\"}, {\"LogCodigo\": \"328\", \"LogDescricao\": \"[#inv0328] - Mensagem retornada pela prefeitura: C\u00f3digo: E001, Mensagem: cvc-pattern-valid: O valor 1 nao tem um aspecto valido em relacao ao padrao [0-9]{6) do tipo TCodigoTribNac.\", \"LogDtaHora\": \"2026-01-20T08:21:59\", \"LogTipo\": 1, \"LogObjeto\": \"PNFS208\", \"ExeAcao\": \"E\", \"ExeWsvServico\": 1, \"ProcessoId\": \"2026012008215786_11339\"}, {\"LogCodigo\": \"328\", \"LogDescricao\": \"[#inv0328] - Mensagem retornada pela prefeitura: C\u00f3digo: E001, Mensagem: cvc-type.3.1.3: O valor 1 do elemento cTribNac nao e valido. Pode estar relacionado \u00e0 tag codTributNacional.\", \"LogDtaHora\": \"2026-01-20T08:21:59\", \"LogTipo\": 1, \"LogObjeto\": \"PNFS208\", \"ExeAcao\": \"E\", \"ExeWsvServico\": 1, \"ProcessoId\": \"2026012008215786_11339\"}, {\"LogCodigo\": \"328\", \"LogDescricao\": \"[#inv0328] - Mensagem retornada pela prefeitura: C\u00f3digo: E001, Mensagem: cvc-complex-type.2.4.a: Foi detectado um conteudo invalido comecando com o elemento pAliqPis. Era esperado um dos {http://www.betha.com.br/e-nota-dps:CST).\", \"LogDtaHora\": \"2026-01-20T08:21:59\", \"LogTipo\": 1, \"LogObjeto\": \"PNFS208\", \"ExeAcao\": \"E\", \"ExeWsvServico\": 1, \"ProcessoId\": \"2026012008215786_11339\"}, {\"LogCodigo\": \"328\", \"LogDescricao\": \"[#inv0328] - Mensagem retornada pela prefeitura: C\u00f3digo: E001, Mensagem: cvc-complex-type.2.4.a: Foi detectado um conteudo invalido comecando com o elemento pAliqPis. Era esperado um dos {http://www.betha.com.br/e-nota-dps:CST). Corre\u00e7\u00e3o: Verifique a estrutura do XML\", \"LogDtaHora\": \"2026-01-20T08:21:59\", \"LogTipo\": 1, \"LogObjeto\": \"PNFS208\", \"ExeAcao\": \"E\", \"ExeWsvServico\": 1, \"ProcessoId\": \"2026012008215786_11339\"}, {\"LogCodigo\": \"328\", \"LogDescricao\": \"[#inv0328] - Mensagem retornada pela prefeitura: C\u00f3digo: E001\", \"LogDtaHora\": \"2026-01-20T08:24:06\", \"LogTipo\": 1, \"LogObjeto\": \"PNFS208\", \"ExeAcao\": \"E\", \"ExeWsvServico\": 1, \"ProcessoId\": \"2026012008240529_96519\"}, {\"LogCodigo\": \"328\", \"LogDescricao\": \"[#inv0328] - Mensagem retornada pela prefeitura: C\u00f3digo: E001, Mensagem: cvc-pattern-valid: O valor 1 nao tem um aspecto valido em relacao ao padrao [0-9]{6) do tipo TCodigoTribNac.\", \"LogDtaHora\": \"2026-01-20T08:24:06\", \"LogTipo\": 1, \"LogObjeto\": \"PNFS208\", \"ExeAcao\": \"E\", \"ExeWsvServico\": 1, \"ProcessoId\": \"2026012008240529_96519\"}, {\"LogCodigo\": \"328\", \"LogDescricao\": \"[#inv0328] - Mensagem retornada pela prefeitura: C\u00f3digo: E001, Mensagem: cvc-type.3.1.3: O valor 1 do elemento cTribNac nao e valido. Pode estar relacionado \u00e0 tag codTributNacional.\", \"LogDtaHora\": \"2026-01-20T08:24:06\", \"LogTipo\": 1, \"LogObjeto\": \"PNFS208\", \"ExeAcao\": \"E\", \"ExeWsvServico\": 1, \"ProcessoId\": \"2026012008240529_96519\"}, {\"LogCodigo\": \"328\", \"LogDescricao\": \"[#inv0328] - Mensagem retornada pela prefeitura: C\u00f3digo: E001, Mensagem: cvc-complex-type.2.4.a: Foi detectado um conteudo invalido comecando com o elemento pAliqPis. Era esperado um dos {http://www.betha.com.br/e-nota-dps:CST).\", \"LogDtaHora\": \"2026-01-20T08:24:06\", \"LogTipo\": 1, \"LogObjeto\": \"PNFS208\", \"ExeAcao\": \"E\", \"ExeWsvServico\": 1, \"ProcessoId\": \"2026012008240529_96519\"}, {\"LogCodigo\": \"328\", \"LogDescricao\": \"[#inv0328] - Mensagem retornada pela prefeitura: C\u00f3digo: E001, Mensagem: cvc-complex-type.2.4.a: Foi detectado um conteudo invalido comecando com o elemento pAliqPis. Era esperado um dos {http://www.betha.com.br/e-nota-dps:CST). Corre\u00e7\u00e3o: Verifique a estrutura do XML\", \"LogDtaHora\": \"2026-01-20T08:24:06\", \"LogTipo\": 1, \"LogObjeto\": \"PNFS208\", \"ExeAcao\": \"E\", \"ExeWsvServico\": 1, \"ProcessoId\": \"2026012008240529_96519\"}], \"Eventos\": []}",
  erro: {
    codigo: "E001",
    mensagem: "cvc-pattern-valid: O valor 1 nao tem um aspecto valido em relacao ao padrao [0-9]{6) do tipo TCodigoTribNac. | cvc-type.3.1.3: O valor 1 do elemento cTribNac nao e valido. Pode estar relacionado \u00e0 tag codTributNacional. | cvc-complex-type.2.4.a: Foi detectado um conteudo invalido comecando com o elemento pAliqPis. Era esperado um dos {\"http://www.betha.com.br/e-nota-dps\":CST)."
  }
};
*/
const PAYLOAD = {
  xml: `<Envio>
	<ModeloDocumento>NFSE</ModeloDocumento>
	<Versao>1.00</Versao>
	<RPS>
		<RPSNumero>2</RPSNumero>
		<RPSSerie>1</RPSSerie>
		<RPSTipo>1</RPSTipo>
		<dEmis>2026-02-23T13:47:16</dEmis>
		<dCompetencia>2026-02-23T13:47:16</dCompetencia>
		<LocalPrestServ>1</LocalPrestServ>
		<natOp>1</natOp>
		<Operacao/>
		<NumProcesso/>
		<benefIdNac/>
		<benefNumero/>
		<RegEspTrib>0</RegEspTrib>
		<OptSN>2</OptSN>
		<regApTribSN/>
		<IncCult>2</IncCult>
		<tpImunidade>0</tpImunidade>
		<tpSusp/>
		<Status>0</Status>
		<cVerificaRPS/>
		<EmpreitadaGlobal/>
		<tpAmb>1</tpAmb>
		<finNFSe>0</finNFSe>
		<indFinal/>
		<cIndOp/>
		<tpEnteGov/>
		<xTpEnteGov/>
		<indDest/>
		<tpOper/>
		<indDoacao/>
		<indZFMALC/>
		<NFSOutrasinformacoes>VALOR REFERENTE A SERVICOS PRESTADOS - Certidão RI 122201; Emolumentos R$27,56; FRJ R$6,26; ISS R$1,38; TOTAL R$35,20.</NFSOutrasinformacoes>
		<cMotivoEmisTI/>
		<chNFSeRej/>
		<RPSCanhoto/>
		<Arquivo/>
		<ExtensaoArquivo/>
		<RPSSubs>
			<SubsNumero/>
			<SubsSerie/>
			<SubsTipo/>
			<SubsNFSeNumero/>
			<SubsDEmisNFSe/>
			<SubsChave/>
			<SubsCodMotivo/>
			<SubsDescMotivo/>
		</RPSSubs>
		<Prestador>
			<CNPJ_prest>12414247134</CNPJ_prest>
			<xNome>REGISTRO DE IMÓVEIS DA COMARCA DE SANTO AMARO DA IMPERATRIZ</xNome>
			<xFant>REGISTRO DE IMÓVEIS DA COMARCA DE SANTO AMARO DA IMPERATRIZ</xFant>
			<IM>4718</IM>
			<IE/>
			<CMC/>
			<CAEPF/>
			<enderPrest>
				<TPEnd>RUA</TPEnd>
				<xLgr>Prefeito Clemente Thiago Diniz</xLgr>
				<nro>110</nro>
				<xCpl/>
				<xBairro>CENTRO</xBairro>
				<cMun>4215703</cMun>
				<UF>SC</UF>
				<CEP>88140000</CEP>
				<fone/>
				<Email>suporte@vhlsistemas.com.br</Email>
			</enderPrest>
		</Prestador>
		<ListaItens>
			<Item>
				<ItemSeq>1</ItemSeq>
				<ItemCod>210101</ItemCod>
				<ItemDesc>VALOR REFERENTE A SERVICOS PRESTADOS - Certidão RI 122201; Emolumentos R$27,56; FRJ R$6,26; ISS R$1,38; TOTAL R$35,20.</ItemDesc>
				<ItemQtde>1</ItemQtde>
				<ItemvUnit>27.56</ItemvUnit>
				<ItemuMed/>
				<ItemvlDed>0.00</ItemvlDed>
				<ItemTributavel/>
				<ItemcCnae>6912500</ItemcCnae>
				<ItemTributMunicipio>210101</ItemTributMunicipio>
				<ItemnAlvara/>
				<ItemvIss>1.38</ItemvIss>
				<ItemvDesconto/>
				<ItemAliquota>0.050000</ItemAliquota>
				<ItemVlrTotal/>
				<ItemBaseCalculo>27.56</ItemBaseCalculo>
				<ItemvlrISSRetido/>
				<ItemIssRetido>2</ItemIssRetido>
				<ItemRespRetencao/>
				<ItemIteListServico>210101</ItemIteListServico>
				<itemCodTributNacional/>
				<ItemExigibilidadeISS>1</ItemExigibilidadeISS>
				<ItemcMunIncidencia>4215703</ItemcMunIncidencia>
				<ItemNumProcesso/>
				<ItemDedTipo/>
				<ItemDedCPFRef/>
				<ItemDedCNPJRef/>
				<ItemDedNFRef/>
				<ItemDedvlTotRef/>
				<ItemDedPer/>
				<ItemDedValor/>
				<ItemVlrLiquido/>
				<ItemValAliqINSS>0.0000</ItemValAliqINSS>
				<ItemValINSS>0</ItemValINSS>
				<ItemValBCINSS/>
				<ItemValAliqIR>0.0000</ItemValAliqIR>
				<ItemValIR>0</ItemValIR>
				<ItemValBCIRRF/>
				<ItemValAliqCOFINS>0.0000</ItemValAliqCOFINS>
				<ItemValCOFINS/>
				<ItemValBCCOFINS/>
				<ItemValAliqCSLL>0.0000</ItemValAliqCSLL>
				<ItemValCSLL>0</ItemValCSLL>
				<ItemValBCCSLL/>
				<ItemValAliqPIS>0.0000</ItemValAliqPIS>
				<ItemValPIS>0</ItemValPIS>
				<ItemValBCPIS/>
				<ItemRedBC/>
				<ItemRedBCRetido/>
				<ItemBCRetido/>
				<ItemValAliqISSRetido>0.0000</ItemValAliqISSRetido>
				<ItemPaisImpDevido/>
				<ItemCST/>
				<ItemJustDed/>
				<ItemvOutrasRetencoes/>
				<ItemDescIncondicionado/>
				<ItemDescCondicionado/>
				<ItemTotalAproxTribServ/>
				<ItemDescHospedagem/>
				<ItemQtdeHospedes/>
				<ItemQtdeDiariasHospedagem/>
				<ItemCodQuartoHospedagem/>
				<ItemDtaEntrHospedagem/>
				<ItemDtaSaiHospedagem/>
				<ItemValorDiariaHospedagem/>
				<ItemCSTPisCofins/>
				<ItemTpRetPisCofins/>
				<ItemNBS/>
			</Item>
		</ListaItens>
		<ListaParcelas/>
		<Servico>
			<IteListServico>210101</IteListServico>
			<Cnae>6912500</Cnae>
			<fPagamento/>
			<tpag/>
			<codTributNacional/>
			<TributMunicipio/>
			<TributMunicDesc/>
			<Discriminacao/>
			<cMun>4215703</cMun>
			<SerQuantidade/>
			<SerUnidade/>
			<SerNumAlvara/>
			<PaiPreServico/>
			<cMunIncidencia/>
			<dVencimento/>
			<ObsInsPagamento/>
			<ObrigoMunic/>
			<TributacaoISS/>
			<CodigoAtividadeEconomica>210101</CodigoAtividadeEconomica>
			<ServicoViasPublicas/>
			<NumeroParcelas/>
			<NroOrcamento/>
			<CodigoNBS>113040000</CodigoNBS>
			<docRef/>
			<idDocTec/>
			<CST/>
			<Valores>
				<ValServicos>27.56</ValServicos>
				<ValPercDeducoes/>
				<ValDeducoes>0.00</ValDeducoes>
				<ValOutrasDeducoes/>
				<ValPIS>0</ValPIS>
				<ValBCPIS/>
				<ValCOFINS/>
				<ValBCCOFINS/>
				<ValINSS>0</ValINSS>
				<ValBCINSS/>
				<ValIR>0</ValIR>
				<ValBCIRRF/>
				<ValCSLL>0</ValCSLL>
				<ValBCCSLL/>
				<RespRetencao/>
				<Tributavel/>
				<ValISS>1.38</ValISS>
				<ISSRetido>2</ISSRetido>
				<ValISSRetido/>
				<ValTotal/>
				<ValTotalRecebido/>
				<ValBaseCalculo>27.56</ValBaseCalculo>
				<ValOutrasRetencoes/>
				<ValAliqISS>0.050000</ValAliqISS>
				<ValAliqPIS>0.0000</ValAliqPIS>
				<PISRetido/>
				<ValAliqCOFINS>0.0000</ValAliqCOFINS>
				<COFINSRetido/>
				<ValAliqIR>0.0000</ValAliqIR>
				<IRRetido/>
				<ValAliqCSLL>0.0000</ValAliqCSLL>
				<CSLLRetido/>
				<ValAliqINSS>0.0000</ValAliqINSS>
				<INSSRetido/>
				<ValAliqCpp/>
				<CppRetido/>
				<ValCpp/>
				<OutrasRetencoesRetido/>
				<ValBCOutrasRetencoes/>
				<ValAliqOutrasRetencoes/>
				<ValAliqTotTributos/>
				<ValLiquido/>
				<ValDescIncond/>
				<ValDescCond/>
				<ValAcrescimos/>
				<ValAliqISSoMunic>0.0000</ValAliqISSoMunic>
				<InfValPIS/>
				<InfValCOFINS/>
				<ValLiqFatura/>
				<ValBCISSRetido/>
				<NroFatura/>
				<CargaTribValor/>
				<CargaTribPercentual/>
				<CargaTribFonte/>
				<JustDed/>
				<ValCredito/>
				<OutrosImp/>
				<ValRedBC/>
				<ValRetFederais/>
				<ValAproxTrib/>
				<NroDeducao/>
				<mdPrestacao/>
				<vincPrest/>
				<tpMoeda/>
				<ValServEst/>
				<mecAFComexP/>
				<mecAFComexT/>
				<movTempBens/>
				<nDI/>
				<nRE/>
				<mdic/>
				<vRecebInterm/>
				<ValRedBenef/>
				<PercRedBenef/>
				<ValRetEstaduais/>
				<ValRetMunicipais/>
				<ValAliqRetFederais/>
				<ValAliqRetEstaduais/>
				<ValAliqRetMunicipais/>
				<ValAproxTribAliqSN/>
				<IBSCBS>
					<ValTotNF/>
					<ValBCIBSCBS/>
					<ValCalcReeRepRes/>
					<ValpRedutor/>
					<ValMulta/>
					<ValJuros/>
					<ValInicialCobrado/>
					<ValFinalCobrado/>
					<ValIPI/>
					<TribRegular>
						<ValpAliqEfeRegIBSUF/>
						<ValTribRegIBSUF/>
						<ValpAliqEfeRegIBSMun/>
						<ValTribRegIBSMun/>
						<ValpAliqEfeRegCBS/>
						<ValTribRegCBS/>
					</TribRegular>
					<TribCompraGov>
						<ValpIBSUF/>
						<ValIBSUF/>
						<ValpIBSMun/>
						<ValIBSMun/>
						<ValpCBS/>
						<ValCBS/>
					</TribCompraGov>
					<IBS>
						<ValIBSTot/>
						<ValCredPresIBS/>
						<ValpCredPresIBS/>
						<ValIBSUF/>
						<ValpIBSUF/>
						<ValDifUF/>
						<ValpDifUF/>
						<ValTribOpUF/>
						<ValpRedAliqUF/>
						<ValpAliqEfetUF/>
						<ValIBSMun/>
						<ValDifMun/>
						<ValpDifMun/>
						<ValDevTribMunIBS/>
						<ValTribOpMun/>
						<ValpAliqEfetMun/>
						<ValpRedAliqMun/>
						<ValpIBSMun/>
						<ValIBSEstCred/>
					</IBS>
					<CBS>
						<ValCBS/>
						<ValpCBS/>
						<ValCredPresCBS/>
						<ValpCredPresCBS/>
						<ValDifCBS/>
						<ValpDifCBS/>
						<ValpAliqEfetCBS/>
						<ValpRedAliqCBS/>
						<ValCBSEstCred/>
					</CBS>
				</IBSCBS>
			</Valores>
			<LocalPrestacao>
				<SerEndTpLgr>RUA</SerEndTpLgr>
				<SerEndLgr>Prefeito Clemente Thiago Diniz</SerEndLgr>
				<SerEndNumero>110</SerEndNumero>
				<SerEndComplemento/>
				<SerEndBairro>CENTRO</SerEndBairro>
				<SerEndxMun/>
				<SerEndcMun>4215703</SerEndcMun>
				<SerEndCep>88140000</SerEndCep>
				<SerEndSiglaUF>SC</SerEndSiglaUF>
			</LocalPrestacao>
			<IBSCBS>
				<cLocalidadeIncid/>
				<xLocalidadeIncid/>
				<CSTIBSCBS/>
				<cClassTrib/>
				<cCredPres/>
				<Onerosidade/>
				<PagParceladoAntecipado/>
				<NCM/>
				<indCompGov/>
				<tpRetPisCofins/>
				<TribRegular>
					<CSTReg/>
					<cClassTribReg/>
				</TribRegular>
			</IBSCBS>
		</Servico>
		<Tomador>
			<TomaCNPJ/>
			<TomaCPF>04188215933</TomaCPF>
			<TomaIE/>
			<TomaIM/>
			<TomaRazaoSocial>DULCE KELLI DE MEDEIROS</TomaRazaoSocial>
			<TomatpLgr/>
			<TomaEndereco>Rua Vereador Augusto Bruggemann</TomaEndereco>
			<TomaNumero>5404</TomaNumero>
			<TomaComplemento/>
			<TomaBairro>CENTRO</TomaBairro>
			<TomacMun/>
			<TomaxMun>Santo Amaro da Imperatri</TomaxMun>
			<TomaUF>SC</TomaUF>
			<TomaPais/>
			<TomaCEP>88140000</TomaCEP>
			<TomaTelefone>48999222334</TomaTelefone>
			<TomaTipoTelefone/>
			<TomaEmail>dulcekelli@gmail.com</TomaEmail>
			<TomaSite/>
			<TomaIME/>
			<TomaSituacaoEspecial/>
			<DocTomadorEstrangeiro/>
			<TomaRegEspTrib/>
			<TomaCadastroMunicipio/>
			<TomaOrgaoPublico/>
			<TomaEnderecoInformado/>
			<TomaCAEPF/>
			<TomaExSemNIF/>
		</Tomador>
		<IntermServico>
			<IntermRazaoSocial/>
			<IntermCNPJ/>
			<IntermCPF/>
			<IntermNIF/>
			<IntermExSemNIF/>
			<IntermIM/>
			<IntermEmail/>
			<IntermEndereco/>
			<IntermNumero/>
			<IntermComplemento/>
			<IntermBairro/>
			<IntermCep/>
			<IntermCmun/>
			<IntermXmun/>
			<IntermFone/>
			<IntermIE/>
			<IntermPais/>
			<IntermUF/>
			<IntermCAEPF/>
		</IntermServico>
		<ConstCivil>
			<CodObra/>
			<Art/>
			<ObraLog/>
			<ObraCompl/>
			<ObraNumero/>
			<ObraBairro/>
			<ObraCEP/>
			<ObraMun/>
			<ObraUF/>
			<ObraPais/>
			<ObraCEI/>
			<ObraMatricula/>
			<ObraValRedBC/>
			<ObraTipo/>
			<ObraNomeFornecedor/>
			<ObraNumeroNF/>
			<ObraDataNF/>
			<ObraNumEncapsulamento/>
			<AbatimentoMateriais/>
			<ObraXMun/>
			<ObraDesc/>
			<ObraCIB/>
			<ObraInscImobFis/>
			<ObraCPFNF/>
			<ObraCNPJNF/>
			<ListaMaterial/>
		</ConstCivil>
		<ListaDed/>
		<Transportadora>
			<TraNome/>
			<TraCPFCNPJ/>
			<TraIE/>
			<TraPlaca/>
			<TraEnd/>
			<TraMun/>
			<TraUF/>
			<TraPais/>
			<TraTipoFrete/>
		</Transportadora>
		<Locacao>
			<categServ/>
			<objetoLocacao/>
			<extensaoFerrovia/>
			<nPostes/>
		</Locacao>
		<AtividadeEvento>
			<AtivDesc/>
			<AtivDataInicial/>
			<AtivDataFinal/>
			<AtivIdEvento/>
			<AtivEndLogradouro/>
			<AtivEndNumero/>
			<AtivEndCompl/>
			<AtivEndBairro/>
			<AtivEndCEP/>
			<AtivEndcMun/>
			<AtivEndxMun/>
			<AtivEndUf/>
		</AtividadeEvento>
		<Pedagio>
			<PedCategVeiculo/>
			<PednEixos/>
			<PedRodagem/>
			<PedSentido/>
			<PedPlaca/>
			<PedCodAcesso/>
			<PedCodContrato/>
		</Pedagio>
		<Destinatario>
			<DestCNPJ/>
			<DestCPF/>
			<DestNIF/>
			<DestcNaoNIF/>
			<DestNome/>
			<DestEndereco/>
			<DestNumero/>
			<DestComplemento/>
			<DestBairro/>
			<DestFone/>
			<DestEmail/>
			<DestcMun/>
			<DestxMun/>
			<DestCEP/>
			<DestPais/>
			<DestEstProvReg/>
		</Destinatario>
		<Imovel/>
		<ListaBensMoveis/>
		<ListaDedIBSCBS/>
		<ListaNFSeRefPagAntecipado/>
	</RPS>
</Envio>`,
  erro: {
    codigo: "E001",
    mensagem: `Erro por não informar codTributNacional
Mensagem: cvc-complex-type.2.4.a: Foi detectado um conteudo invalido comecando com o elemento cNBS. Era esperado um dos {http://www.betha.com.br/e-nota-dps:cTribNac). Correção: Verifique a estrutura do XML

Erro por não estar informada a discriminação
Mensagem: cvc-complex-type.2.4.a: Foi detectado um conteudo invalido comecando com o elemento infoCompl. Era esperado um dos {http://www.betha.com.br/e-nota-dps:cServ).

Erro por não informar a tag TomacMun
Mensagem: cvc-complex-type.2.4.a: Foi detectado um conteudo invalido comecando com o elemento CEP. Era esperado um dos {http://www.betha.com.br/e-nota-dps:cMun).`
  }
};

const body = JSON.stringify(PAYLOAD);

const options = {
  hostname: "localhost",
  port: 8000,
  path: "/diagnostico",
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Content-Length": Buffer.byteLength(body)
  }
};

console.log("Enviando para http://localhost:8000/diagnostico...");
console.log("Codigo erro:", PAYLOAD.erro.codigo);
console.log("Mensagem:", PAYLOAD.erro.mensagem.slice(0, 100) + "...");
console.log("(O agente pode levar 30-120s)");
console.log("");

const req = http.request(options, (res) => {
  let data = "";
  res.on("data", (chunk) => data += chunk);
  res.on("end", () => {
    console.log("HTTP", res.statusCode);
    console.log("");
    try {
      const r = JSON.parse(data);
      console.log("=== DIAGNOSTICO ===");
      console.log("Status:          ", r.status);
      console.log("Classificacao:   ", r.metadata?.classificacao);
      console.log("Confianca:       ", r.metadata?.confianca);
      console.log("Erro catalogado: ", r.metadata?.erro_catalogado);
      console.log("Tempo (ms):      ", r.tempo_processamento_ms);
      console.log("");
      console.log("--- Tags com problema ---");
      (r.tags_com_problema || []).forEach((t, i) => {
        console.log(`  [${i+1}] ${t.tag}`);
        console.log(`      Enviado: ${t.valor_enviado}`);
        console.log(`      Correto: ${t.valor_correto}`);
        console.log(`      Motivo:  ${(t.explicacao||"").slice(0, 120)}`);
      });
      console.log("");
      console.log("--- Solucao ---");
      console.log("  Resumo:", r.solucao?.resumo);
      (r.solucao?.passos || []).forEach(p => console.log(" ", p));
      if (r.solucao?.xml_corrigido) {
        console.log("");
        console.log("  XML corrigido:", r.solucao.xml_corrigido);
      }
      console.log("");
      console.log("=== JSON COMPLETO ===");
      console.log(JSON.stringify(r, null, 2));
    } catch {
      console.log("Resposta raw:", data);
    }
  });
});

req.on("error", (err) => {
  console.error("Erro:", err.message);
  console.error("Verifique se a API esta rodando: uvicorn app.main:app --port 8000");
});

req.setTimeout(300000, () => {
  console.error("Timeout (5 min)");
  req.destroy();
});

req.write(body);
req.end();
