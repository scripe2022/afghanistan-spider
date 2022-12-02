import seq from 'sequelize';
import config from './config.json' assert {type: 'json'};
import http from 'http';
import querystring from 'querystring';
import * as deepl from 'deepl-node';

const { Sequelize } = seq;

const sequelize = new Sequelize(config.dbname, config.user, config.password, {
    host: config.host,
    dialect: 'mysql',
});

const Posts = sequelize.define("posts", {
    id: {
        type: Sequelize.INTEGER,
        autoIncrement: true,
        primaryKey: true,
        allowNull: false
    },
    url: Sequelize.STRING(300),
    datetime: Sequelize.STRING(50),
    title: Sequelize.STRING(300),
    titletrans: Sequelize.STRING(300),
    type: Sequelize.STRING(50),
    content: Sequelize.JSON,
    }, {
    tableName: 'posts',
    timestamps: false
});

const translate = async(text) => {
    const authKey = "482567eb-d972-8b04-20df-1f01f7fefe09:fx";
    const translator = new deepl.Translator(authKey);
    const result = await translator.translateText(text, null, 'zh');
    return result.text;
}
for (let i = 151; i <= 200; ++i) {
    const result = await Posts.findAll({
        where: {
            id: i
        }
    })
    let post = result[0].dataValues;
    const n = post.content.length;
    for (let j = 0; j < n; ++j) {
        let temp = await translate(post.content[j]);
        post.content.push(temp);
    }
    let newtitle = await translate(post.title);
    await Posts.update({
        titletrans: newtitle,
        content: post.content,
    }, {
        where: {
            id: i
        }
    })
}