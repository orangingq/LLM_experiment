examples = [
    {
        "sentence": "세종대왕은 책을 좋아했다.",
        "output":
            """
            (a:사람 {{name: '세종대왕'}})
            (a)-[:좋아했다]->(:책)
            """
    }, {
        "sentence": "학생 A는 선생님께 과제를 냈다.",
        "output":
            """
            (a:사람 {{name: '학생 A'}})
            (a)-[:제출했다 {{to: (:선생님)}}]->(:과제)
            """
    }, {
        "sentence": "왕 씨는 지난 6일에 위층 베란다에 남자아이가 매달려 있는 상황을 목격했다.",
        "output":
            """
            (a:사람 {{name: '왕 씨'}})
            (b:장소 {{name: '위층 베란다'}})
            (c:사람 {{성별: '남자', 연령: '아이'}})
            (c)-[:매달리다]->(b)
            (a)-[:목격했다 {{시간: '지난 6일'}}]->(c)
            """
    }, {
        "sentence": "왕 씨는 지난 6일에 위층 베란다에 남자아이가 매달려 있는 상황을 목격했다. 왕 씨는 지방 당국에 신고했다. 지방 당국은 왕씨 일가에게 용감한 시민상을 수여했다.",
        "output":
            """
            (a:사람 {{name: '왕 씨'}})
            (b:장소 {{name: '위층 베란다'}})
            (c:사람 {{성별: '남자', 연령: '아이'}})
            (d:기관 {{name: '지방 당국'}})
            (e:상 {{name: '용감한 시민상'}})
            (f:사람들 {{name: '왕씨 일가'}})
            (c)-[:매달리다]->(b)
            (a)-[:목격했다 {{시간: '지난 6일'}}]->(c)
            (a)-[:신고했다 {{to: (d)}}]->(c)
            (d)-[:수여했다 {{to: (f)}}]->(e)
            """
    }
]