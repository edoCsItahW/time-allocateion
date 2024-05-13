#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/9 上午9:06
# 当前项目名: pyAndWeb
# 编码模式: utf-8
# 注释: 
# -------------------------<edocsitahw>----------------------------
from flask import Flask, render_template

app = Flask(__name__, static_folder=r".\static", template_folder=r".\template")


@app.route("/", methods=["GET", "POST"])
def root():
    return render_template(r"UI.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

