package lucene;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Date;
import java.util.Scanner;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Date;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.fa.PersianAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;

/** Simple command-line based search demo. */
public class SearchFiles {

  
	private SearchFiles() {}

  /** Simple command-line based search demo. */
  public static void main(String[] args) throws Exception {
    String usage =
      "Usage:\tjava org.apache.lucene.demo.SearchFiles [-index dir] [-field f] [-repeat n] [-queries file] [-query string] [-raw] [-paging hitsPerPage]\n\nSee http://lucene.apache.org/core/4_1_0/demo/ for details.";
    if (args.length > 0 && ("-h".equals(args[0]) || "-help".equals(args[0]))) {
      System.out.println(usage);
      System.exit(0);
    }

    String index = "Shafilou_index";
    String field = "contents";
    String queries = null;
    int repeat = 0;
    boolean raw = false;
    String queryString = null;
    int hitsPerPage = 10;
    
    for(int i = 0;i < args.length;i++) {
     if ("-index".equals(args[i])) {
        index = args[i+1];
        i++;
      } else if ("-field".equals(args[i])) {
        field = args[i+1];
        i++;
      } else if ("-queries".equals(args[i])) {
        queries = args[i+1];
        i++;
      } else if ("-query".equals(args[i])) {
        queryString = args[i+1];
        i++;
      } else if ("-repeat".equals(args[i])) {
        repeat = Integer.parseInt(args[i+1]);
        i++;
      } else if ("-raw".equals(args[i])) {
        raw = true;
      } else if ("-paging".equals(args[i])) {
        hitsPerPage = Integer.parseInt(args[i+1]);
        if (hitsPerPage <= 0) {
          System.err.println("There must be at least 1 hit per page.");
          System.exit(1);
        }
        i++;
      }
    }
    
    IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(index)));
    IndexSearcher searcher = new IndexSearcher(reader);
    File file = new File("stopword"); 
    
    BufferedReader br = new BufferedReader(new FileReader(file)); 
    ArrayList<String> lines=new ArrayList<String>();
    String st; 
    while ((st = br.readLine()) != null) {
  	  lines.add(st);
    } 
    CharArraySet stopSet = new CharArraySet(lines, false);
//    System.out.println(stopSet);
    Analyzer analyzer = new PersianAnalyzer(stopSet);

    BufferedReader in = null;
    if (queries != null) {
      in = Files.newBufferedReader(Paths.get(queries), StandardCharsets.UTF_8);
    } else {
      in = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
    }
    QueryParser parser = new QueryParser(field, analyzer);
    while (true) {
      if (queries == null && queryString == null) {                        // prompt the user
        System.out.println("Enter text of document you search for: ");
      }

     String line = queryString != null ? queryString : in.readLine();

      if (line == null || line.length() == -1) {
        break;
      }

      line = line.trim();
      if (line.length() == 0) {
        break;
      }
      
      Query query = parser.parse(line);
//      System.out.println("Searching for: " + query.toString(field));
            
      if (repeat > 0) {                           // repeat & time as benchmark
        Date start = new Date();
        for (int i = 0; i < repeat; i++) {
          searcher.search(query, 100);
        }
        Date end = new Date();
        System.out.println("Time: "+(end.getTime()-start.getTime())+"ms");
      }

      doPagingSearch(in, searcher, query, hitsPerPage, raw, queries == null && queryString == null);

      if (queryString != null) {
        break;
      }
    }
    reader.close();
  }

  /**
139   * This demonstrates a typical paging search scenario, where the search engine presents 
140   * pages of size n to the user. The user can then go to the next page if interested in
141   * the next hits.
142   * 
143   * When the query is executed for the first time, then only enough results are collected
144   * to fill 5 result pages. If the user wants to page beyond this limit, then the query
145   * is executed another time and all hits are collected.
 * @throws Exception 
   * 
   */
  public static void doPagingSearch(BufferedReader in, IndexSearcher searcher, Query query, 
                                     int hitsPerPage, boolean raw, boolean interactive) throws IOException, Exception {
 
	  Class.forName("com.mysql.cj.jdbc.Driver");
	  Connection connect = DriverManager
              .getConnection("jdbc:mysql://localhost/docs?useUnicode=true&characterEncoding=UTF-8&"
                      + "user=root&password=");
	  Statement statement = connect.createStatement();
	  String stmt="SELECT * FROM documents WHERE ";

	  String date="";
	  String category="";
	  String Title="";
	  ArrayList<String> docDB=new ArrayList<String>();
	  ArrayList<String> db=new ArrayList<String>();
	  Scanner sc = new Scanner(System.in);
	  System.out.println("Do you want to search with additional fields:(y/n) ");
	  String otherField=sc.nextLine();
	  if(otherField.equals("y")) {
		 System.out.println("Enter date");
		 date=sc.nextLine();
		 System.out.println("Enter category");
		 category=sc.nextLine();
		 System.out.println("Enter title");
		 Title=sc.nextLine();
	  }
	  if(!date.equals("")) {
		  stmt+="date LIKE '%"+date+"%' ";
	  }
	  if(!category.equals("")) {
		  if(stmt.indexOf("date")==-1)
			  stmt+="category LIKE '%"+category+"%' "; 
		  else
			  stmt+=" OR category LIKE '%"+category+"%' ";
	  }
	  if(!Title.equals("")) {
		  if((stmt.indexOf("date")==-1)&&(stmt.indexOf("category")==-1))
			  stmt+="title LIKE '%"+Title+"%'";
		  else
			  stmt+="OR title LIKE '%"+Title+"%'";

	  }
	  System.out.println(stmt);
	  if(otherField.equals("y")){
	  ResultSet resultSet = statement.executeQuery(stmt);
//	  System.out.println("hello");
	  while (resultSet.next()) {
		  docDB.add(resultSet.getString("id"));
//		  String id = resultSet.getString("id");
//		  System.out.println(id);
	  }
//	  System.out.println(docDB);
	  }
	  // 1Collect enough docs to show 5 pages
    TopDocs results = searcher.search(query, 5 * hitsPerPage);
    ScoreDoc[] hits = results.scoreDocs;
//    System.out.println(hits);
    
    int numTotalHits = Math.toIntExact(results.totalHits);
//    System.out.println(numTotalHits + " total matching documents");

    int start = 0;
    int end = Math.min(numTotalHits, hitsPerPage);
        
    while (true) {
      if (end > hits.length) {
        System.out.println("Only results 1 - " + hits.length +" of " + numTotalHits + " total matching documents collected.");
        System.out.println("Collect more (y/n) ?");
        String line = in.readLine();
        if (line.length() == 0 || line.charAt(0) == 'n') {
          break;
        }

        hits = searcher.search(query, numTotalHits).scoreDocs;
      }
      
      end = Math.min(hits.length, start + hitsPerPage);
      
      for (int i = start; i < end; i++) {
        if (raw) {                              // output raw format
//          System.out.println("doc="+hits[i].doc+" score="+hits[i].score);
          continue;
        }
        for(int j=0;j<docDB.size();j++) {
//       	System.out.println("hit is: "+hits[i].doc+" doc: "+docDB.get(j));
        	if(Integer.parseInt(docDB.get(j))==hits[i].doc) {
//        		System.out.println("final doc="+hits[i].doc+" score="+hits[i].score);
        		stmt="SELECT * FROM documents WHERE id="+docDB.get(j);
        		ResultSet resultSet = statement.executeQuery(stmt);
        		  while (resultSet.next()) {
        			  System.out.println("document id is: "+resultSet.getString("id"));
        			  System.out.println("date is:\n"+resultSet.getString("date"));
        			  System.out.println("title is:\n "+resultSet.getString("title"));
        			  System.out.println("text is:\n"+resultSet.getString("text"));
//        			 
        		  }
        		}}
        Document doc = searcher.doc(hits[i].doc);
        String path = doc.get("path");
        if (path != null) {
//          System.out.println((i+1) + ". " + path);
//          System.out.println("hello");
//        	System.out.println("doc="+hits[i].doc+" score="+hits[i].score);
          String title = doc.get("title");
          if (title != null) {
            System.out.println("   Title: " + doc.get("title"));
          }
        } else {
          System.out.println((i+1) + ". " + "No path for this document");
        }
                  
      }
      	connect.close();
      if (!interactive || end == 0) {
        break;
      }

      if (numTotalHits >= end) {
        boolean quit = false;
        while (true) {
          System.out.print("Press ");
          if (start - hitsPerPage >= 0) {
            System.out.print("(p)revious page, ");  
          }
          if (start + hitsPerPage < numTotalHits) {
            System.out.print("(n)ext page, ");
          }
          System.out.println("(q)uit or enter number to jump to a page.");
          
          String line = in.readLine();
         if (line.length() == 0 || line.charAt(0)=='q') {
           quit = true;
            break;
          }
          if (line.charAt(0) == 'p') {
           start = Math.max(0, start - hitsPerPage);
            break;
          } else if (line.charAt(0) == 'n') {
            if (start + hitsPerPage < numTotalHits) {
              start+=hitsPerPage;
            }
            break;
          } else {
            int page = Integer.parseInt(line);
            if ((page - 1) * hitsPerPage < numTotalHits) {
              start = (page - 1) * hitsPerPage;
              break;
            } else {
              System.out.println("No such page");
            }
          }
        }
        if (quit) break;
        end = Math.min(numTotalHits, start + hitsPerPage);
      }
    }
  }
}