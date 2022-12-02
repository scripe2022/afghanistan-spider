import seq from 'sequelize';
import config from './config.json' assert {type: 'json'};
import http from 'http';
import querystring from 'querystring';

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

for (let i = 101; i <= 363; ++i) {
    console.log(i);
    const result = await Posts.findAll({
        where: {
            id: i
        }
    })
    let post = result[0].dataValues;
    const n = post.content.length;
    let new_content = []
    for (let j = 0; j < n; ++j) {
        if (post.content[j] != '') {
            new_content.push(post.content[j]);
        }
    }
    await Posts.update({
        content: new_content
    }, {
        where: {
            id: i
        }
    })
}