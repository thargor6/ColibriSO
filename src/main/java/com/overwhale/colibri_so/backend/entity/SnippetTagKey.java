package com.overwhale.colibri_so.backend.entity;

import lombok.Data;

import java.io.Serializable;
import java.util.UUID;

@Data
public class SnippetTagKey implements Serializable {
  private UUID snippetId;
  private UUID tagId;
}
