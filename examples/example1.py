examples = [
    {
        "sentence": "세종대왕은 책을 좋아했다.",
        "output":
            """
            :세종대왕 :좋아했다 :책 .
            """
    }, {
        "sentence": "학생 A는 선생님께 과제를 냈다.",
        "output":
            """
            :A :직업 :학생 .
            << :A :제출했다 :과제 >> :to :선생님 .
            """
    }, {
        "sentence": "왕 씨는 지난 6일에 위층 베란다에 남자아이가 매달려 있는 상황을 목격했다.",
        "output":
            """
            << :왕_씨 :목격했다 << :남자아이 :매달려_있다 :위층_베란다 >> >> :에 :지난_6일 .
            """
    }, {
        "sentence": "왕 씨는 지난 6일에 위층 베란다에 남자아이가 매달려 있는 상황을 목격했다. 왕 씨는 지방 당국에 신고했다. 지방 당국은 왕씨 일가에게 용감한 시민상을 수여했다.",
        "output":
            """
            << :왕_씨 :목격했다 << :남자아이 :매달려_있다 :위층_베란다 >> >> :에 :지난_6일 .
            << :왕_씨 :신고했다 << :남자아이 :매달려_있다 :위층_베란다 >> >> :에 :지방_당국 .
            << :지방_당국 :수여했다 :용감한_시민상 >> :에게 :왕씨_일가 .
            """
    }
]
