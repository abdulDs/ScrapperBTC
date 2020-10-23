bash installMongoBash.sh



mongo<<EOF
use admin;
db.createUser(
    {
        user: "root1234",
        pwd: "password",
        roles: ["root"]
    }
);
EOF


python3 btcScrapperMongodb.py
