diff --git a/HeapSnapshot.js b/HeapSnapshot.js
index 6301a18..2133f18 100644
--- a/HeapSnapshot.js
+++ b/HeapSnapshot.js
@@ -1452,6 +1452,37 @@ WebInspector.HeapSnapshot.prototype = {
         }
     },
 
+    // The algorithm is based on the article:
+    // A. L. Buchsbaum, H. Kaplan and A Rogers "Linear-Time Pointer-Machine Algorithms
+    // for Least Common Ancestors, MST Verification, and Dominators"
+    // Proc. of the 30th Annual Symposium on Theory of Computing (STOC'98), pp. 279-288.
+    /**
+     * @param {Array.<number>} postOrderIndex2NodeOrdinal
+     * @param {Array.<number>} nodeOrdinal2PostOrderIndex
+     */
+    _buildDominatorTree_Buchsbaum: function(postOrderIndex2NodeOrdinal, nodeOrdinal2PostOrderIndex)
+    {
+        var idom = new Uint32Array(nodesCount); // dominators
+        var bucketHeads = new Uint32Array(nodesCount + 1);  // Initialized with 0.
+        var bucketTails = new Uint32Array(nodesCount + 1);  // Initialized with 0.
+        for (var postOrderIndex = rootPostOrderedIndex - 1; postOrderIndex >= 0; --postOrderIndex) {
+            nodeOrdinal = postOrderIndex2NodeOrdinal[postOrderIndex];
+            if (/* iidom(nodeOrdinal) is included in micro(nodeOrdinal) */) {
+                idom[nodeOrdinal] = iidom(nodeOrdinal);
+            } else {
+                // Add nodeOrdinal to bucket[pxdom(nodeOrdinal)].
+                this._addToSet(bucketHeads, bucketTails, pxdom(nodeOrdinal), nodeOrdinal);
+            }
+        }
+        for (var postOrderIndex = rootPostOrderedIndex - 1; postOrderIndex >= 0; --postOrderIndex) {
+            nodeOrdinal = postOrderIndex2NodeOrdinal[postOrderIndex];
+            if (nodeOrdinal /* is a trivial microtree */) {
+                Process2();
+                link(nodeOrdinal);
+            }
+        }
+    },
+
     _calculateRetainedSizes: function(postOrderIndex2NodeOrdinal)
     {
         var nodeCount = this.nodeCount;
