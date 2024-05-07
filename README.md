![banner](https://github.com/nvsriram/KeeperVision/assets/50625504/56e69ee3-a7d9-413a-85f4-f73253c34675)

## 💡Motivation

Soccer is the most popular sport with hundreds of millions of players and fans around the world. Many times, a key save can be the difference between winning and losing a game. KeeperVision is a training tool which aims to help goalkeepers in tackling their greatest hurdle - positioning. Using computer vision, image processing, and machine learning, KeeperVision physically guides goalkeepers in real-time to the best position to defend against any incoming shots.

## 🌐 API Reference

### `api/register/<username>`

<details>   
<summary><b>GET</b></summary>
   <table>
      <tr>
         <th rowspan="3">Response</th>
         <th>OK</th>
         <th>Code</th>
         <th>Content</th>
      </tr>
      <tr>
         <td>✅</td>
         <td><code>200</code></td>
         <td>
            <pre lang="typescript">{"id": &lt;player_id&gt;}</pre>
         </td>
      </tr>
      <tr>
         <td>❌</td>
         <td><code>404</code></td>
         <td>
            <pre lang="typescript">{"message": "Player &lt;username&gt; does not exist."}</pre>
         </td>
      </tr>
   </table> 
</details>

<details>
<summary><b>POST</b></summary>
   <table>
      <tr>
         <th>Body</th>
         <td colspan='4'>
            <pre lang="typescript">{"email": &lt;email&gt;}</pre>
         </td>
      </tr>
      <tr>
         <th rowspan='4'>Response</th>
         <th>OK</th>
         <th>Code</th>
         <th>Content</th>
      </tr>
      <tr>
         <td>✅</td>
         <td><code>200</code></td>
         <td>
            <pre lang="typescript">{"id": &lt;player_id&gt;}</pre>
         </td>
      </tr>
      <tr>
         <td>❌</td>
         <td><code>400</code></td>
         <td>
            <pre lang="typescript">{"message": "&lt;some error message like duplicate key Integrity error&gt;"}</pre>
         </td>
      </tr>
   </table>
</details>

### `api/session/<username>`

<details>   
<summary><b>GET</b></summary>
   <table>
      <tr>
         <th rowspan='3'>Response</th>
         <th>OK</th>
         <th>Code</th>
         <th>Content</th>
      </tr>
      <tr>
         <td>✅</td>
         <td><code>200</code></td>
         <td>
            <pre lang="typescript">{"player_id": &lt;player_id&gt;, "session_stats": &lt;list of session_stats in desc order of session_end&gt;}</pre>
         </td>
      </tr>
      <tr>
         <td>❌</td>
         <td><code>404</code></td>
         <td>
            <pre lang="typescript">{"message": "Player &lt;username&gt; does not exist."}</pre>
         </td>
      </tr>
   </table> 
</details>

<details>
<summary><b>POST</b></summary>
   <table>
      <tr>
         <th>Body</th>
         <td colspan='4'>
            <pre lang="typescript">{"session_stats": &lt;session_stats JSON with all the fields&gt;}</pre>
         </td>
      </tr>
      <tr>
         <th rowspan='3'>Files</th>
         <th>File Name</th>
         <th colspan='4'>Description</th>
      </tr>
      <tr>
         <td><code>initial_image</code></td>
         <td colspan='4'>Image file containing goalkeeper's initial position before session starts</td>
      </tr>
      <tr>
         <td><code>final_image</code></td>
         <td colspan='4'>Image file containing goalkeeper's final position at the end of session</td>
      </tr>
      <tr>
         <th rowspan='4'>Response</th>
         <th>OK</th>
         <th>Code</th>
         <th>Content</th>
      </tr>
      <tr>
         <td>✅</td>
         <td><code>200</code></td>
         <td>
            <pre lang="typescript">{"id": &lt;session_id&gt;}</pre>
         </td>
      </tr>
      <tr>
         <td>❌</td>
         <td><code>400</code></td>
         <td>
            <pre lang="typescript">{"message": "&lt;some error message like duplicate key Integrity error&gt;"}</pre>
         </td>
      </tr>
      <tr>
         <td>❌</td>
         <td><code>404</code></td>
         <td>
            <pre lang="typescript">{"message": "Player &lt;username&gt; does not exist."}</pre>
         </td>
      </tr>
   </table>
</details>

### `api/predict`

<details>   
<summary><b>POST</b></summary>
   <table>
      <tr>
         <th rowspan='2'>Files</th>
         <th>File Name</th>
         <th colspan='2'>Description</th>
      </tr>
      <tr>
         <td><code>image</code></td>
         <td colspan='2'>Image file to be processed</td>
      </tr>
      <tr>
         <th rowspan='4'>Response</th>
         <th>OK</th>
         <th>Code</th>
         <th>Content</th>
      </tr>
      <tr>
         <td>✅</td>
         <td><code>200</code></td>
         <td>
            <pre lang="typescript">{"idx": &lt;idx corresponding to direction to move&gt;, "x": &lt;offset in x direction&gt;, "y": &lt;offset in y direction&gt;}</pre>
         </td>
      </tr>
   </table>
</details>

## 📈 Block Diagram

![Block Diagram 2](https://github.com/nvsriram/KeeperVision/assets/50625504/b5c1cec2-a9f0-4b01-8828-41b061232a9e)



## 💻 Instructions on running locally

1. Ensure python is installed
2. Run `pip install -r requirements.txt` to install all dependencies<br />
   **NOTE:** Recommended to use venv before installing dependencies. See below for details on how to set it up
3. Run the Flask app using `python app.py`. This will run the app on debug mode on the server's IP<br />
   **NOTE**: Ensure the Flask app and the client are in the same WLAN to be able to connect to the server's IP as it is otherwise considered a private IP address

**[Optional]** To use venv:

1. Run `python -m venv <path-to-env>` to create virtual environment
2. To activate the virtual environment:

   - If on Windows, run: `<path-to-env>/Scripts/activate`
   - If on MacOS, run: `source <path-to-env>/bin/activate`

3. Run Step 2 to install all dependencies
