db.createCollection("films", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         title: "Reviews and likes Object Validation",
         required: [ "film_id"],
         properties: {
            film_id: {
               bsonType: "string",
               description: "'film_id' must be a string and is required"
            },
            likes: {
              bsonType: "object",
              properties:
              {
                up: {
                  bsonType: "object",
                  properties: {
                    count: { bsonType: "int" },
                    ids: { bsonType: "array" }
                  }
                },
                down: {
                  bsonType: "object",
                  properties: {
                    count: { bsonType: "int" },
                    ids: { bsonType: "array" }
                  }
                }
              }
            }
         }
      }
   }
})


db.createCollection("rating", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Rating Object Validation",
            properties: {
                film_id: {bsonType: "string"},
                rating: {bsonType: "int"},
                user_id: {bsonType: "string"},
            }
        }
    }
}

)

db.rating.createIndex({"user_id": 1}, {unique: true})

db.createCollection("bookmarks", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         title: "Bookmarks Object Validation",
            properties: {
              film_id: {bsonType: "array", uniqueItems: true},
              user_id: { bsonType: "string" },
        }
    }
  }
})

db.createCollection("reviews", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         title: "Reviews Object Validation",
            properties: {

              film_id: {bsonType: "string"},
              review_id: {bsonType: "string", },
              user_id: { bsonType: "string" },
              firstname: { bsonType: "string" },
              lastname: { bsonType: "string" },
              created: { bsonType: "date" },
              mark: { bsonType: "int" },
              text: { bsonType: "string" },
              review_evaluation: {
                bsonType: "object",
                properties:
                {
                  up: {
                    bsonType: "object",
                    properties: {
                      count: { bsonType: "int" },
                      ids: { bsonType: "array" }
                    }
                  },
                  down: {
                    bsonType: "object",
                    properties: {
                      count: { bsonType: "int" },
                      ids: { bsonType: "array" }
                    }
                  }
                }

              }
        }
    }
  }
})