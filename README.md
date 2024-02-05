# KeeperVision

## API Reference

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
            <pre><code class="lang-javascript">{<span class="hljs-attr">"id"</span>: <span class="hljs-string">&lt;player_id&gt;</span>}</code></pre>
         </td>
      </tr>
      <tr>
         <td>❌</td>
         <td><code>404</code></td>
         <td>
            <pre><code class="lang-javascript">{<span class="hljs-attr">"message"</span>: <span class="hljs-string">"Player &lt;username&gt; does not exist."</span>}</code></pre>
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
            <pre><code class="lang-json">{<span class="hljs-attr">"email"</span>: <span class="hljs-string">&lt;email&gt;</span>}</code></pre>
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
            <pre><code class="lang-json">{<span class="hljs-attr">"id"</span>: <span class="hljs-string">&lt;player_id&gt;</span>}</code></pre>
         </td>
      </tr>
      <tr>
         <td>❌</td>
         <td><code>400</code></td>
         <td>
            <pre><code class="lang-json">{<span class="hljs-attr">"message"</span>: <span class="hljs-string">"&lt;some error message like duplicate key Integrity error&gt;"</span>}</code></pre>
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
            <pre><code class="lang-json">{<span class="hljs-attr">"player_id"</span>: <span class="hljs-string">&lt;player_id&gt;</span>, <span class="hljs-attr">"session_stats"</span>: <span class="hljs-string">&lt;list of session_stats in desc order of session_end&gt;</span>}</code></pre>
         </td>
      </tr>
      <tr>
         <td>❌</td>
         <td><code>404</code></td>
         <td>
            <pre><code class="lang-json">{<span class="hljs-attr">"message"</span>: <span class="hljs-string">"Player &lt;username&gt; does not exist."</span>}</code></pre>
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
            <pre><code class="lang-json">{<span class="hljs-attr">"session_stats"</span>: <span class="hljs-string">&lt;session_stats JSON with all the fields&gt;</span>}</code></pre>
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
            <pre><code class="lang-json">{<span class="hljs-attr">"id"</span>: <span class="hljs-string">&lt;session_id&gt;</span>}</code></pre>
         </td>
      </tr>
      <tr>
         <td>❌</td>
         <td><code>400</code></td>
         <td>
            <pre><code class="lang-json">{<span class="hljs-attr">"message"</span>: <span class="hljs-string">"&lt;some error message like duplicate key Integrity error&gt;"</span>}</code></pre>
         </td>
      </tr>
      <tr>
         <td>❌</td>
         <td><code>404</code></td>
         <td>
            <pre><code class="lang-json">{<span class="hljs-attr">"message"</span>: <span class="hljs-string">"Player &lt;username&gt; does not exist."</span>}</code></pre>
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
            <pre><code class="lang-json">{<span class="hljs-attr">"idx"</span>: <span class="hljs-string">&lt;idx corresponding to direction to move&gt;</span>, <span class="hljs-attr">"x"</span>: <span class="hljs-string">&lt;offset in x direction&gt;</span>, <span class="hljs-attr">"y"</span>: <span class="hljs-string">&lt;offset in y direction&gt;</span>}</code></pre>
         </td>
      </tr>
   </table>
</details>

## Instructions on running locally

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
