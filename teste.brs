{
    papo_que idade = 20
    papo_que nome = "Zé"
    papo_que ta_bebado = fatos

    manda_ae(idade)
    manda_ae(nome)

    cpa (idade >= 18) {
        manda_ae("Pode beber, meu chapa!")
    }
    caducou {
        manda_ae("Vai tomar coca-cola!")
    }

    boh (idade < 23) {
        cpa (idade == 21) {
            sai_fora
        }
        idade = idade + 1
        manda_ae(idade)
    }
}
