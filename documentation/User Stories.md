* As an user, I can log in and add my food items and the best before date to the application so that I can track what I currently have and if any of it is expiring.  

* As an user, I can see my items being ordered by the best before date, so I can quickly see what is going to expire soon.  
``` SELECT user_item.id AS id, user_item.name AS name, user_item.best_before AS best_before FROM item, user_item ```  
``` WHERE user_item.account_id = :user```  
```AND user_item.used = false```  
```AND user_item.expired = false```  
```GROUP BY user_item.id```  
```ORDER BY (CASE WHEN user_item.best_before IS NULL THEN 1 ELSE 0 END) ASC, user_item.best_before ASC```  

* As an user, I can mark my food items used, expired or delete them so that my view of items stays updated.  

* As an user, I can create new recipes.

* As an user, I can see all the recipes created on the application in an order depending on items already owned.
```SELECT recipe.id, recipe.name, recipe.image, COUNT(DISTINCT ingredient.id)```  
                    ``` FROM item CROSS JOIN user_item CROSS JOIN account CROSS JOIN recipe```  
                    ``` LEFT JOIN ingredient```  
                    ``` ON ingredient.recipe_id = recipe.id```  
                    ``` AND ingredient.item_id = item.id```  
                    ``` AND item.id = user_item.item_id```  
                    ``` AND user_item.expired = false```  
                    ``` AND user_item.used = false```  
                    ``` AND user_item.account_id = :userId```  
                    ``` GROUP BY recipe.id, recipe.name, recipe.image```  
                    ``` ORDER BY COUNT(ingredient.id) DESC```  

* As an user, I can see recipes that use a specific item I own in an order depending on items already owned.  
```SELECT recipe.id, recipe.name, recipe.image, COUNT(DISTINCT ingredient.id)```  
                    ``` FROM item CROSS JOIN user_item CROSS JOIN account CROSS JOIN recipe```  
                    ``` LEFT JOIN ingredient ON recipe.id = ingredient.recipe_id```  
                    ``` AND ingredient.item_id = item.id```  
                    ``` AND item.id = user_item.item_id```  
                    ``` AND user_item.expired = false```  
                    ``` AND user_item.used = false```  
                    ``` AND user_item.account_id = :userId```  
                    ``` WHERE recipe.id IN (```  
                    ```  SELECT recipe.id FROM recipe, ingredient, user_item, item```  
                    ```  WHERE recipe.id = ingredient.recipe_id"```  
                    ```  AND ingredient.item_id = item.id"```  
                    ```  AND item.id = user_item.item_id```  
                    ```  AND user_item.id = :user_itemId)```  
                    ``` GROUP BY recipe.id, recipe.name, recipe.image```  
                    ``` ORDER BY COUNT(ingredient.id) DESC```  

* As an user, I can delete and edit recipes that I created.

* As an admin, I can delete and edit recipes by other users.
